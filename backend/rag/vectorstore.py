import chromadb
from chromadb.config import Settings
from .models import Document
from .settings import get_settings

class ChromaVectorStore:
    def __init__(self) -> None:
        settings = get_settings()

        self.client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=settings.chroma_path
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
        )

    def add_document(self, doc: Document):
        self.collection.add(
            ids=[doc.id],
            documents=[doc.content],
            metadatas=[doc.metadata],
        )

    def query(self, text: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        return results
