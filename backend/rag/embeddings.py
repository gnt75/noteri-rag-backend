
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from .config import get_settings

def get_embedding_function():
    settings = get_settings()
    return SentenceTransformerEmbeddingFunction(model_name=settings.embedding_model)
