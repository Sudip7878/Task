from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from typing import List, Dict, Any
import uuid

class VectorStore:
    def __init__(self):
        # Using memory storage for reliability in this environment
        self.client = QdrantClient(":memory:")
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # Ensure collection exists
        self.client.recreate_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    def upsert_chunks(self, chunks: List[str], metadata: Dict[str, Any]):
        embeddings = self.model.encode(chunks)
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={"text": chunk, **metadata}
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points
        )

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_vector = self.model.encode(query).tolist()
        results = self.client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=limit
        ).points
        return [{"text": res.payload["text"], "score": getattr(res, 'score', 0), "metadata": res.payload} for res in results]

vector_store = VectorStore()
