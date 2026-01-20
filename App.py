import streamlit as st
import math
from datetime import date
from datetime import datetime
import pytz
from protocols.protocol_fnc import load_protocol_markdown
from setting import qa_chain


st.title("HỎI ĐÁP PHÁC ĐỒ HÓA TRỊ")

protocol_list = [
    "Acute Lymphoblastic Leukemia - Thông tin chung"
    "Acute Lymphoblastic Leukemia - SR - IND",
    "Acute Lymphoblastic Leukemia - SR - CON",
    "Acute Lymphoblastic Leukemia - SR - IM1",
    "Acute Lymphoblastic Leukemia - SR - DI",
    "Acute Lymphoblastic Leukemia - SR - IM2",
    "Acute Lymphoblastic Leukemia - SR - M",
    "Acute Lymphoblastic Leukemia - HR - IND",
    "Acute Lymphoblastic Leukemia - HR - CON",
    "Acute Lymphoblastic Leukemia - HR - IM1",
    "Acute Lymphoblastic Leukemia - HR - DI",
    "Acute Lymphoblastic Leukemia - HR - IM2",
    "Acute Lymphoblastic Leukemia - HR - M",

    "Lymphoma thông tin chung"
    "Lymphoma - group A",
    "Lymphoma - group B - COP",
    "Lymphoma - group B - COPADM#1",
    "Lymphoma - group B - COPADM#2",
    "Lymphoma - group B - CYM#1",      
    "Lymphoma - group B - CYM#2",    

    "Lymphoma - group C - COP",
    "Lymphoma - group C - R-COPADM#1",
    "Lymphoma - group C - R-COPADM#2",
    "Lymphoma - group C (CNS-) - R-CYVE#1",       
    "Lymphoma - group C (CNS-) - R-CYVE#2",  
    "Lymphoma - group C (CNS+) - R-CYVE#1",
    "Lymphoma - group C (CNS+) - HMTX",     
    "Lymphoma - group C (CNS+) - R-CYVE#2", 
    "Lymphoma - group C - M1",
    "Lymphoma - group C - M2",
    "Lymphoma - group C - M3",
    "Lymphoma - group C - M4",
]

with st.form(key='protocol_form'):
    age = st.number_input(
        "Nhập tuổi (năm)",
        min_value=1,
        max_value=18,
        step=1,
        value=None
    )

    wt = st.number_input(
        "Cân nặng (kg)",
        min_value=1.0,
        max_value=120.0,
        step=0.1,
        value=None
    )

    ht = st.number_input(
        "Chiều cao (cm)",
        min_value=20.0,
        max_value=200.0,
        step=0.1,
        value=None
    )

    if wt is not None and ht is not None:
        bsa = math.sqrt(wt * ht / 3600)
    
    protocol_code = st.selectbox(
        "Tên phác đồ hóa trị",
        options=protocol_list,
    )

    query = st.text_area("Đặt câu hỏi về phác đồ hóa trị", height="content")

    submit = st.form_submit_button('Thực hiện')

if submit and age and wt and ht and bsa and protocol_code :
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(tz)
    
    base_info = {
        "age": age,
        "weight": wt,
        "height": ht,
        "bsa": round(bsa, 3),
        "now": now
    }

    protocol_text = load_protocol_markdown(protocol_code)

    with st.expander("📄 Nội dung phác đồ"):
        st.markdown(protocol_text)
    
    with st.spinner("Đang suy nghĩ ...", show_time=True):
        answer = qa_chain(
            base_info=base_info, 
            query=query, 
            context=protocol_text
        )
        
        st.markdown(answer)

    



