import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chat import ChatMessage
from app.models.user import User
from app.rag.llm import get_llm
from app.rag.prompt import build_rag_prompt
from app.schemas.chat import AskRequest, AskResponse
from app.services.cache_service import cache_service
from app.services.vector_service import search_user_documents


def ask_question(db: Session, user: User, payload: AskRequest) -> AskResponse:
    if not cache_service.check_rate_limit(user.id):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

    cache_key = cache_service.question_key(user.id, payload.question)
    cached = cache_service.get_json(cache_key)
    if cached:
        cached["cached"] = True
        return AskResponse(**cached)

    results = search_user_documents(user.id, payload.question, settings.RETRIEVAL_TOP_K)
    sources = []
    for doc, score in results:
        sources.append(
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "score": round(float(score), 4),
                "document_id": int(doc.metadata["document_id"]) if doc.metadata.get("document_id") else None,
            }
        )

    llm = get_llm()
    prompt = build_rag_prompt(payload.question, sources) if sources else payload.question
    answer = llm.invoke(prompt).content

    response = {"answer": answer, "sources": sources, "cached": False}
    cache_service.set_json(cache_key, {"answer": answer, "sources": sources}, settings.QA_CACHE_TTL_SECONDS)

    db.add(ChatMessage(user_id=user.id, session_id=payload.session_id, role="user", content=payload.question))
    db.add(
        ChatMessage(
            user_id=user.id,
            session_id=payload.session_id,
            role="assistant",
            content=answer,
            sources_json=json.dumps(sources, ensure_ascii=False),
        )
    )
    db.commit()
    return AskResponse(**response)
