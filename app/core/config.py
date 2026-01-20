from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG & Ingestion API"
    
    # API Keys
    GROQ_API_KEY: str
    LANGCHAIN_API_KEY: Optional[str] = None
    HF_TOKEN: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Vector DB
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "documents"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # LLM Config
    LLM_MODEL: str = "llama-3.1-8b-instant"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
