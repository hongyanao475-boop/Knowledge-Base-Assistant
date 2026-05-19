import logging

from langchain_community.vectorstores import Chroma

from app.core.config import settings
from app.rag.embeddings import ZhipuAIEmbeddings


logger = logging.getLogger(__name__)
_vectorstore = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=str(settings.CHROMA_PATH),
            embedding_function=ZhipuAIEmbeddings(),
        )
    return _vectorstore


def add_chunks(user_id: int, document_id: int, filename: str, chunks) -> int:
    vectorstore = get_vectorstore()
    ids = []
    for idx, chunk in enumerate(chunks):
        chunk.metadata.update(
            {
                "user_id": str(user_id),
                "document_id": str(document_id),
                "source": filename,
                "chunk_index": idx,
            }
        )
        ids.append(f"doc-{document_id}-chunk-{idx}")
    vectorstore.add_documents(chunks, ids=ids)
    try:
        vectorstore.persist()
    except Exception:
        logger.debug("Chroma persist skipped by current version")
    return len(chunks)


def search_user_documents(user_id: int, question: str, top_k: int):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search_with_relevance_scores(
        question,
        k=top_k,
        filter={"user_id": str(user_id)},
    )
