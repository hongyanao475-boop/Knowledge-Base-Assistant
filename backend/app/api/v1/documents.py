from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.document import DocumentOut, DocumentUploadResponse
from app.services.document_service import delete_user_document, list_user_documents, save_upload
from app.tasks.document_tasks import index_document_task


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=201)
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = save_upload(db, current_user, file)
    background_tasks.add_task(index_document_task, document.id)
    return DocumentUploadResponse(
        id=document.id,
        filename=document.filename,
        status=document.status,
        message="Upload received. Indexing has started in background.",
    )


@router.get("", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_user_documents(db, current_user)


@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_user_document(db, current_user, document_id)
