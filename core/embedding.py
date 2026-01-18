import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from typing import List
from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStore
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings


@st.cache_resource(show_spinner=True)    
def create_index_with_cache(store_id: str, _docs: List[Document]) -> VectorStore:
    index = FAISS.from_documents(
        documents=_docs, 
        # embedding=OpenAIEmbeddings(model="text-embedding-3-large")
        # embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        embedding=OpenAIEmbeddings()
    )
    return index
# store_id chỉ có vai trò trong quá trình cache_resource

