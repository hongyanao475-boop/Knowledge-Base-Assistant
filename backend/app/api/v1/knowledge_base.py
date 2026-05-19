from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.document import Document
from app.models.user import User


router = APIRouter(prefix="/knowledge-bases", tags=["knowledge-bases"])


@router.get("/status")
def get_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total = db.query(Document).filter(Document.user_id == current_user.id).count()
    indexed = db.query(Document).filter(Document.user_id == current_user.id, Document.status == "indexed").count()
    indexing = db.query(Document).filter(Document.user_id == current_user.id, Document.status == "indexing").count()
    failed = db.query(Document).filter(Document.user_id == current_user.id, Document.status == "failed").count()
    return {
        "status": "ready" if indexed > 0 else "empty",
        "document_count": total,
        "indexed_count": indexed,
        "indexing_count": indexing,
        "failed_count": failed,
    }
