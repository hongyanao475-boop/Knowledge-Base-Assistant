from typing import List, Optional

from pydantic import BaseModel, Field


class SourceChunk(BaseModel):
    content: str
    source: str
    score: float
    document_id: Optional[int] = None


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    session_id: Optional[int] = None


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceChunk] = []
    cached: bool = False
