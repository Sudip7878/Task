import PyPDF2
from typing import BinaryIO
from io import BytesIO
from sqlmodel import Session
from app.db.models import DocumentMetadata
from app.utils.chunkers import get_chunker
from app.utils.vector_store import vector_store
import os

class IngestionService:
    def extract_text(self, file: BinaryIO, filename: str) -> str:
        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif filename.endswith(".txt"):
            return file.read().decode("utf-8")
        else:
            raise ValueError("Unsupported file type")

    def process_document(
        self, 
        file_content: bytes, 
        filename: str, 
        strategy: str, 
        chunk_size: int, 
        chunk_overlap: int,
        db: Session
    ):
        text = self.extract_text(BytesIO(file_content), filename)
        chunker = get_chunker(strategy)
        chunks = chunker.chunk(text, chunk_size, chunk_overlap)
        
        # Store in Vector DB
        metadata = {
            "filename": filename,
            "strategy": strategy,
        }
        vector_store.upsert_chunks(chunks, metadata)
        
        # Store metadata in SQL DB
        doc_meta = DocumentMetadata(
            filename=filename,
            chunking_strategy=strategy,
            file_type="pdf" if filename.endswith(".pdf") else "txt",
            num_chunks=len(chunks)
        )
        db.add(doc_meta)
        db.commit()
        db.refresh(doc_meta)
        
        return doc_meta

ingestion_service = IngestionService()
