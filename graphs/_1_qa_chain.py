from typing import Dict
from setting import get_rag_model, rag_prompt_template
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain

# chọn ra từ kho lưu trữ 10 bài Doc liên quan nhất, sau đó áp dụng Weighted Reciprocal Rank Fusion (RRF) để chọn ra 5 tài liệu cuối cùng 
# Cơ chế của Weighted Reciprocal Rank Fusion (RRF): cân đối giữa dense + sparse retrieval
# lambda_mult = 1.0 → rely entirely on dense embedding similarity
# lambda_mult = 0.0 → rely entirely on keyword / sparse similarity
# lambda_mult = 0.6 → a mix (60% weight to dense similarity, 40% to sparse similarity)

model = get_rag_model()

rag_prompt = PromptTemplate(
    template=rag_prompt_template,
    input_variables=["input", "context"]
)

def generate_answer(question: str, vector_store: Dict, base_info: Dict):

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,
            "fetch_k": 10,
            # "lambda_mult": 0.6,
            "lambda_mult": 0.2,
        }
    )

    docs = retriever.invoke(question)

    prompt_input = {
        "base_info": str(base_info),
        "input": question,
        "context": docs
    }

    answer = (
        rag_prompt
        | model
        | StrOutputParser()
    ).invoke(prompt_input)

    return {
        "answer": answer,
        "context": docs
    }
