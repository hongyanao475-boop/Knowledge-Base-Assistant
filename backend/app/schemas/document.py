from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    status: str
    error_msg: Optional[str] = None
    chunk_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    status: str
    message: str
