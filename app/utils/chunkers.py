from typing import List, Protocol
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Chunker(Protocol):
    def chunk(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        ...

class SimpleCharacterChunker:
    def chunk(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        chunks = []
        for i in range(0, len(text), chunk_size - chunk_overlap):
            chunks.append(text[i : i + chunk_size])
        return chunks

class RecursiveCharacterChunker:
    def chunk(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_text(text)

def get_chunker(strategy: str) -> Chunker:
    if strategy == "recursive":
        return RecursiveCharacterChunker()
    return SimpleCharacterChunker()
