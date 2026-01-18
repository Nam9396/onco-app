import streamlit as st
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from copy import deepcopy
from pathlib import Path
from hashlib import md5
import re

from langchain_core.documents import Document


class File(ABC):
    def __init__(
        self,
        name: str,
        id: str,
        docs: List[Document],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.id = id
        self.docs = docs
        self.metadata = metadata or {}

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"

    def copy(self):
        return self.__class__(
            name=self.name,
            id=self.id,
            docs=deepcopy(self.docs),
            metadata=deepcopy(self.metadata),
        )



def clean_doc(text: str, removed_words: List[str] | None = None) -> str:
    text = re.sub(r"[ \t]+", " ", text).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)

    if removed_words:
        pattern = r"\b(?:" + "|".join(map(re.escape, removed_words)) + r")\b"
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text


def split_mdx_by_heading(text: str):
    """
    Split MD/MDX by headings (#, ##, ###)
    """
    pattern = r"(#{1,3}\s.+)"
    parts = re.split(pattern, text)

    sections = []
    for i in range(1, len(parts), 2):
        title = parts[i].lstrip("#").strip()
        content = parts[i + 1].strip()

        if len(content) >= 200:
            sections.append(
                {
                    "title": title,
                    "content": content,
                }
            )
    return sections


class MdxProtocolFile(File):
    @classmethod
    def from_path(
        cls,
        path: Path,
        removed_words: List[str] | None = None,
    ) -> "MdxProtocolFile":

        raw_text = path.read_text(encoding="utf-8")
        cleaned_text = clean_doc(raw_text, removed_words)

        sections = split_mdx_by_heading(cleaned_text)

        docs: List[Document] = []
        for i, sec in enumerate(sections):
            doc = Document(
                page_content=sec["content"],
                metadata={
                    "protocol": path.stem,
                    "section": sec["title"],
                    "order": i + 1,
                    "source": path.name,
                },
            )
            docs.append(doc)

        return cls(
            name=path.name,
            id=md5(raw_text.encode()).hexdigest(),
            docs=docs,
            metadata={"protocol": path.stem},
        )


@st.cache_data(show_spinner=True)
def load_protocol(protocol_name: str, protocol_dir: Path) -> MdxProtocolFile:
    path = protocol_dir / f"{protocol_name}.md"

    if not path.exists():
        raise FileNotFoundError(f"Protocol {protocol_name} not found")

    return MdxProtocolFile.from_path(path)
