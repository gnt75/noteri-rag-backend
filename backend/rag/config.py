
import os
from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):
    # Path on disk where Chroma will persist the index
    chroma_path: str = os.getenv("CHROMA_PATH", "chroma_db")
    # Name of the collection inside Chroma
    collection_name: str = os.getenv("CHROMA_COLLECTION", "noteri_docs")
    # Embedding model to use
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> "Settings":
    return Settings()
