from pathlib import Path
import streamlit as st

PROTOCOL_REGISTRY = {
# bạch cầu cấp
    "Acute Lymphoblastic Leukemia - Thông tin chung": "all/LYMPH",
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
    "Lymphoma thông tin chung": "lymphoma/LYMPH",  
    "Lymphoma - group A": "lymphoma/1_LYMPH_A_COPAD", 
    "Lymphoma - group B - COP": "lymphoma/1_LYMPH_B_COP", 
    "Lymphoma - group B - COPADM#1": "lymphoma/2_LYMPH_B_COPADM1",
    "Lymphoma - group B - COPADM#2": "lymphoma/3_LYMPH_B_COPADM2",
    "Lymphoma - group B - CYM#1": "lymphoma/4_LYMPH_B_CYM1",       
    "Lymphoma - group B - CYM#2": "lymphoma/5_LYMPH_B_CYM2",    

    "Lymphoma - group C - COP": "lymphoma/_1_LYMPH_C_COP", 
    "Lymphoma - group C - R-COPADM#1": "lymphoma/_2_LYMPH_C_COPADM1",
    "Lymphoma - group C - R-COPADM#2": "lymphoma/_3_LYMPH_C_COPADM2",
    "Lymphoma - group C (CNS-) - R-CYVE#1": "lymphoma/_4_LYMPH_C_CYVE1_NEG",       
    "Lymphoma - group C (CNS-) - R-CYVE#2": "lymphoma/_5_LYMPH_C_CYVE2_NEG",  
    "Lymphoma - group C (CNS+) - R-CYVE#1": "lymphoma/_6_LYMPH_C_CYVE1_POS",
    "Lymphoma - group C (CNS+) - HMTX": "lymphoma/_7_LYMPH_C_HMTX",       
    "Lymphoma - group C (CNS+) - R-CYVE#2": "lymphoma/_8_LYMPH_C_CYVE2_POS",  
    "Lymphoma - group C - M1": "lymphoma/_9_LYMPH_C_M1",
    "Lymphoma - group C - M2": "lymphoma/_10_LYMPH_C_M2",
    "Lymphoma - group C - M3": "lymphoma/_11_LYMPH_C_M3",
    "Lymphoma - group C - M4": "lymphoma/_12_LYMPH_C_M4",
}


@st.cache_data(show_spinner=False)
def load_protocol_markdown(protocol_code):
    protocol_uri = Path("protocols") / f"{PROTOCOL_REGISTRY[protocol_code]}.md"
    return protocol_uri.read_text(encoding="utf-8") 
