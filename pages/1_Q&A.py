import streamlit as st
import time 
from pathlib import Path

from core.md_parsing import load_protocol
from core.embedding import create_index_with_cache
from graphs._1_qa_chain import generate_answer
from components.ui import display_general_error, display_general_warning, display_retry_loop_error

st.title("Hỏi đáp về phác đồ hóa trị")

if not st.session_state.get("ready_for_dosing"):
    st.warning("Vui lòng nhập thông tin bệnh nhi và chọn phác đồ trước.")
    st.stop()

# trích xuất thông tin phác đồ / bệnh nhân 

base_info = st.session_state["base_info"]

if "protocol" not in st.session_state:
    st.error("Chưa chọn phác đồ hóa trị.")
    st.stop()

PROTOCOL_REGISTRY = {
# bạch cầu cấp
    "Acute Lymphoblastic Leukemia - SR - IND": "all/1_ALL_SR_IND",
    "Acute Lymphoblastic Leukemia - SR - CON": "all/2_ALL_SR_CON",
    "Acute Lymphoblastic Leukemia - SR - IM1": "all/3_ALL_SR_IM1",
    "Acute Lymphoblastic Leukemia - SR - DI": "all/4_ALL_SR_DI",
    "Acute Lymphoblastic Leukemia - SR - IM2": "all/5_ALL_SR_IM2",
    "Acute Lymphoblastic Leukemia - SR - M": "all/6_ALL_SR_M",
    "Acute Lymphoblastic Leukemia - HR - IND": "all/1_ALL_HR_IND",
    "Acute Lymphoblastic Leukemia - HR - CON": "all/2_ALL_HR_CON",
    "Acute Lymphoblastic Leukemia - HR - IM1": "all/3_ALL_HR_IM1",
    "Acute Lymphoblastic Leukemia - HR - DI": "all/4_ALL_HR_DI",
    "Acute Lymphoblastic Leukemia - HR - IM2": "all/5_ALL_HR_IM2",
    "Acute Lymphoblastic Leukemia - HR - M": "all/6_ALL_HR_M",
# lymphoma
    "Lymphoma nguy cơ thấp (group A)": "lymphoma/1_LYMPH_A_COPAD", 
    "Lymphoma nguy cơ trung bình (group B) - COP": "lymphoma/1_LYMPH_B_COP", 
    "Lymphoma nguy cơ trung bình (group B) - COPADM#1": "lymphoma/2_LYMPH_B_COPADM1",
    "Lymphoma nguy cơ trung bình (group B) - COPADM#2": "lymphoma/3_LYMPH_B_COPADM2",
    "Lymphoma nguy cơ trung bình (group B) - CYM#1": "lymphoma/4_LYMPH_B_CYM1",       
    "Lymphoma nguy cơ trung bình (group B) - CYM#2": "lymphoma/5_LYMPH_B_CYM2",    

    "Lymphoma nguy cơ cao (group C) - COP": "lymphoma/_1_LYMPH_C_COP", 
    "Lymphoma nguy cơ cao (group C) - R-COPADM#1": "lymphoma/_2_LYMPH_C_COPADM1",
    "Lymphoma nguy cơ cao (group C) - R-COPADM#2": "lymphoma/_3_LYMPH_C_COPADM2",
    "Lymphoma nguy cơ cao (group C) (CNS-) - R-CYVE#1": "lymphoma/_4_LYMPH_C_CYVE1_NEG",       
    "Lymphoma nguy cơ cao (group C) (CNS-) - R-CYVE#2": "lymphoma/_5_LYMPH_C_CYVE2_NEG",  
    "Lymphoma nguy cơ cao (group C) (CNS+) - R-CYVE#1": "lymphoma/_6_LYMPH_C_CYVE1_POS",
    "Lymphoma nguy cơ cao (group C) (CNS+) - HMTX": "lymphoma/_7_LYMPH_C_HMTX",       
    "Lymphoma nguy cơ cao (group C) (CNS+) - R-CYVE#2": "lymphoma/_8_LYMPH_C_CYVE2_POS",  
    "Lymphoma nguy cơ cao (group C) - M1": "lymphoma/_9_LYMPH_C_M1",
    "Lymphoma nguy cơ cao (group C) - M2": "lymphoma/_10_LYMPH_C_M2",
    "Lymphoma nguy cơ cao (group C) - M3": "lymphoma/_11_LYMPH_C_M3",
    "Lymphoma nguy cơ cao (group C) - M4": "lymphoma/_12_LYMPH_C_M4",
}

PROTOCOL_DIR = Path("protocols")
protocol_name = PROTOCOL_REGISTRY[st.session_state["protocol"]]  
protocol_file = PROTOCOL_DIR / f"{protocol_name}.md"

if not protocol_file.exists():
    st.error(f"Không tìm thấy phác đồ: {protocol_name}")
    st.stop()

@st.cache_data(show_spinner=False)
def load_protocol_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")

protocol_text = load_protocol_markdown(protocol_file)

if protocol_text:
    if "protocol_text" not in st.session_state:
        st.session_state["protocol_text"] = protocol_text
else: 
    st.error(f"Lỗi khi tải phác đồ phác đồ: {protocol_name}")
    st.stop()


with st.expander("📄 Nội dung phác đồ"):
    st.markdown(protocol_text)

protocol_file = load_protocol(protocol_name, PROTOCOL_DIR)

if len(protocol_file.docs) == 0:
    display_general_warning(message="File không có nội dung hoặc nội dung.")

with st.form(key='qa_form'):
        query = st.text_area("Đặt câu hỏi về phác đồ hóa trị")
        submit = st.form_submit_button("Thực hiện")


if submit and query:

    with st.spinner("Đang xử lý ... Vui lòng đợi trong giây lát⏳", show_time=True):     
        try: 
            vector_store = create_index_with_cache(store_id=protocol_file.id, _docs=protocol_file.docs)
        except Exception as e: 
            display_general_error(e=e, message="Phát sinh lỗi trong quá trình lập chỉ mục nội dung. Nguyên nhân: file bị lỗi hoặc liên quan đến mạng.")
            
        response = None

        for attempt in range(3):
            try:
                response = generate_answer(question=query, vector_store=vector_store, base_info=base_info)
                break
            except Exception as e:
                display_retry_loop_error(e)
                time.sleep(2)
        
        if response is None:
            st.error(f"[FAILED] Thất bại sau 3 lần thử. Bấm tải lại chương trình sau vài phút.")
            st.stop()
    
        st.markdown("#### CÂU TRẢ LỜI")

        st.markdown(response["answer"])

        st.markdown("---")
        
        with st.expander("TRÍCH DẪN NGUỒN TÀI LIỆU"):
            for doc in response["context"]:
                metadata_values = list(doc.metadata.values())
                metadata_info = f"**File: {metadata_values[0]} - {metadata_values[1]} - {metadata_values[2]} - {metadata_values[3]}**"        
                st.markdown(metadata_info)
                st.write(doc.page_content)
                st.markdown("-----")
        
    

        


