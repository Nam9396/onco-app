import streamlit as st
import math
from datetime import date
from datetime import datetime
import pytz


st.title("CHỌN CHỦ ĐỀ HÓA TRỊ")

# important functions

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    # giảm 1 nếu sinh nhật năm nay chưa tới
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

protocol_list = [
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

    "Lymphoma nguy cơ thấp (group A)",
    "Lymphoma nguy cơ trung bình (group B) - COP",
    "Lymphoma nguy cơ trung bình (group B) - COPADM#1",
    "Lymphoma nguy cơ trung bình (group B) - COPADM#2",
    "Lymphoma nguy cơ trung bình (group B) - CYM#1",      
    "Lymphoma nguy cơ trung bình (group B) - CYM#2",    

    "Lymphoma nguy cơ cao (group C) - COP",
    "Lymphoma nguy cơ cao (group C) - R-COPADM#1",
    "Lymphoma nguy cơ cao (group C) - R-COPADM#2",
    "Lymphoma nguy cơ cao (group C) (CNS-) - R-CYVE#1",       
    "Lymphoma nguy cơ cao (group C) (CNS-) - R-CYVE#2",  
    "Lymphoma nguy cơ cao (group C) (CNS+) - R-CYVE#1",
    "Lymphoma nguy cơ cao (group C) (CNS+) - HMTX",     
    "Lymphoma nguy cơ cao (group C) (CNS+) - R-CYVE#2", 
    "Lymphoma nguy cơ cao (group C) - M1",
    "Lymphoma nguy cơ cao (group C) - M2",
    "Lymphoma nguy cơ cao (group C) - M3",
    "Lymphoma nguy cơ cao (group C) - M4",
]

if "protocol" not in st.session_state:
    st.session_state["protocol"] = None 

# form section

with st.form(key='protocol_form'):
    age = st.number_input(
        "Nhập tuổi (năm)",
        min_value=1,
        max_value=18,
        step=1,
        value=None,
        placeholder="Nhập tuổi (năm)",
    )
    wt = st.number_input(
        "Cân nặng (kg)",
        min_value=1.0,
        max_value=120.0,
        step=0.1,
        value=None,
        placeholder="Nhập cân nặng",
        help="Giá trị phù hợp cho bệnh nhi (1 – 120 kg)"
    )
    ht = st.number_input(
        "Chiều cao (cm)",
        min_value=20.0,
        max_value=200.0,
        step=0.1,
        value=None,
        placeholder="Nhập chiều cao",
        help="Giá trị phù hợp cho bệnh nhi (20–200 cm)"
    )
    if wt is not None and ht is not None:
        bsa = math.sqrt(wt * ht / 3600)
    protocol = st.selectbox(
        "Tên phác đồ hóa trị",
        options=protocol_list,
        index=0 if st.session_state["protocol"] is None else protocol_list.index(st.session_state["protocol"])
    )

    submit = st.form_submit_button('Thực hiện')

if submit and age and wt and ht and bsa and protocol :
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(tz)
    
    st.session_state["base_info"] = {
        "age": age,
        "weight": wt,
        "height": ht,
        "bsa": round(bsa, 3),
        "now": now
    }
    
    st.session_state["protocol"] = protocol
    st.session_state["ready_for_dosing"] = True
    st.switch_page("pages/1_Q&A.py")
