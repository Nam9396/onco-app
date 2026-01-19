import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

# rag_prompt_template = """
# Nhiệm vụ của bạn là đọc phác đồ hóa trị và hỗ trợ bác sĩ đưa ra các quyết định điều trị. 

# ### Hướng dẫn suy nghĩ (chạy nền) 
# -   Kiểm tra điều kiện: giai đoạn bệnh, ngày hóa trị, tuổi; khi xác định thuốc cần dùng
# -	Xem xét dữ kiện cung cấp, đối chiếu với phác đồ. 

# ### Về cách trình bày:
# 1.	Bố cục câu trả lời ngắn gọn, sử dụng **headings, bullet points**, or **numbered sections** nếu cần thiết.
# 2.  Nêu những điểm chưa rõ ràng hoặc còn thiếu thông tin cần thiết

# ### Lưu ý quan trọng: 
# - **CHỈ** sử dụng thông tin trong phần **Nguồn tài liệu**.
# - **KHÔNG ĐƯỢC** bao gồm kiến thức chung, giả định, hoặc diễn giải cá nhân.
# - Nếu **Nguồn tài liệu** không đủ để trả lời câu hỏi, hãy thừa nhận giới hạn của câu trả lời.

# ---
# **Thông tin nền**:
# {base_info}

# **Câu hỏi**: {input}

# **Nguồn tài liệu**:
# {context}
# """

rag_prompt_template = """
Nhiệm vụ của bạn là đọc phác đồ hóa trị và hỗ trợ bác sĩ đưa ra các quyết định điều trị. 

### Các bước suy nghĩ (chạy nền) 
- Kiểm tra điều kiện: giai đoạn bệnh, ngày hóa trị, tuổi; khi xác định thuốc cần dùng
- Xem xét dữ kiện cung cấp, đối chiếu với phác đồ. 

### Về cách trình bày:
1. Bố cục câu trả lời thật ngắn gọn
2. sử dụng **headings, bullet points**, or **numbered sections** nếu cần thiết.

### Lưu ý quan trọng: 
- **CHỈ** sử dụng thông tin trong phần **Nguồn tài liệu**.
- Nếu **Nguồn tài liệu** không đủ để trả lời câu hỏi, hãy thừa nhận giới hạn của câu trả lời.

---
**Thông tin nền**:
{base_info}

**Câu hỏi**: {input}

**Nguồn tài liệu**:
{context}
"""


@st.cache_resource(show_spinner=True)
def get_rag_model():
    return ChatOpenAI(
        model=st.session_state.get("LLM_MODEL", "gpt-5-mini"),
        api_key=OPENAI_API_KEY,
        temperature=0.2,
        # top_p=0.9,
        # presence_penalty=0.1,
        # frequency_penalty=0.2
    )
