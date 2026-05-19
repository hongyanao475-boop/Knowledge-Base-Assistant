from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document
from app.models.user import User


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}


def save_upload(db: Session, user: User, file: UploadFile) -> Document:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
        )

    user_dir = settings.UPLOAD_DIR / str(user.id)
    user_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename or "document").name
    target = user_dir / f"{int(datetime.utcnow().timestamp())}_{safe_name}"

    size = 0
    with target.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > settings.MAX_UPLOAD_MB * 1024 * 1024:
                target.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="File too large")
            buffer.write(chunk)

    document = Document(
        user_id=user.id,
        filename=safe_name,
        file_path=str(target),
        file_type=suffix.lstrip("."),
        file_size=size,
        status="pending",
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def list_user_documents(db: Session, user: User) -> List[Document]:
    return (
        db.query(Document)
        .filter(Document.user_id == user.id)
        .order_by(Document.created_at.desc())
        .all()
    )


def delete_user_document(db: Session, user: User, document_id: int) -> None:
    document = db.query(Document).filter(Document.id == document_id, Document.user_id == user.id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    Path(document.file_path).unlink(missing_ok=True)
    db.delete(document)
    db.commit()
