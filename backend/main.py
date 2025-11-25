
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from rag.engine import RagEngine

app = FastAPI(title="Noteri-im RAG API")

rag_engine = RagEngine()

class DocumentIn(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: Optional[Dict[str, Any]] = None

class RagQuery(BaseModel):
    question: str
    top_k: int = 4

@app.get("/")
def health_check():
    return {"message": "Noteri-im RAG API is running"}

@app.post("/documents")
def add_document(doc: DocumentIn):
    """
    Add or update a document in the vector store.
    """
    try:
        doc_id = rag_engine.add_document(
            text=doc.text,
            metadata=doc.metadata or {},
            id=doc.id,
        )
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag")
def rag_query(payload: RagQuery):
    """
    Simple RAG endpoint:
    - retrieves top_k most similar chunks
    - returns a naive answer + the retrieved chunks as sources
    """
    try:
        answer, sources = rag_engine.answer_question(
            question=payload.question,
            top_k=payload.top_k,
        )
        return {
            "question": payload.question,
            "answer": answer,
            "sources": sources,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
