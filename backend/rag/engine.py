
from typing import List, Tuple, Dict, Any

from .vectorstore import ChromaVectorStore

class RagEngine:
    def __init__(self) -> None:
        self.vs = ChromaVectorStore()

    def add_document(self, text: str, metadata: Dict[str, Any], id: str | None = None) -> str:
        return self.vs.add_document(text=text, metadata=metadata, id=id)

    def answer_question(self, question: str, top_k: int = 4) -> Tuple[str, List[Dict[str, Any]]]:
        results = self.vs.query(question=question, top_k=top_k)

        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        sources: List[Dict[str, Any]] = []
        for i, doc in enumerate(docs):
            sources.append(
                {
                    "id": ids[i] if i < len(ids) else None,
                    "text": doc,
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                }
            )

        # Naive "answer": just concatenation of the retrieved chunks
        if docs:
            answer = " ".join(docs)
        else:
            answer = "Nuk gjeta dot nje pergjigje nga dokumentet. Shto me shume dokumente ose pyet ndryshe."

        return answer, sources
