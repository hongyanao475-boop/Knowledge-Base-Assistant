from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.chat import AskRequest, AskResponse
from app.services.chat_service import ask_question


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ask_question(db, current_user, payload)
