import streamlit as st 
import os 
from dotenv import load_dotenv
load_dotenv()

def sidebar():
    with st.sidebar:

        # API Key input section
        api_key_input = st.text_input(
            label="OpenAI API Key", 
            type="password",
            placeholder="Nhập API key (sk-....)", 
            help="Bạn có thể đăng ký API key ở https://platform.openai.com/account/api-keys",
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", None)
        )
        st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("------")

        if not api_key_input: 
            st.warning("Bạn cần nhập API key để sử dụng app")

        # Model options section
        llm_model = st.selectbox(
            label="Chọn LLM model",
            options=["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4o-mini", "gpt-3.5-turbo"]
        )        
        st.session_state["LLM_MODEL"] = llm_model

        # Chọn truy xuất dữ liệu hay không 
        show_citation = st.radio(
            "Xem dẫn nguồn của câu trả lời", 
            options=["Ẩn nguồn tài liệu", "Hiển thị nguồn tài liệu"], 
        )
        st.session_state["show_citation"] = show_citation


        # Chọn tự đánh giá câu trả lời hay không 
        show_evaluation = st.radio(
            "Xem phản biện câu trả lời",   
            options=["Ẩn phản biện", "Hiển thị phản biện"], 
        )
        st.session_state["show_evaluation"] = show_evaluation

        # Chọn hiển thị dẫn nguồn đoạn văn
        show_paragraph_source = st.radio(
            "Xem dẫn nguồn đoạn văn", 
            options=["Ẩn nguồn đoạn văn", "Hiển thị nguồn đoạn văn"]
        )
        st.session_state["show_paragraph_source"] = show_paragraph_source
