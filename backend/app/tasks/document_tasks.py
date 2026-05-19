import logging
from datetime import datetime

from app.db.session import SessionLocal
from app.models.document import Document
from app.rag.loader import load_file
from app.rag.splitter import split_documents
from app.services.vector_service import add_chunks


logger = logging.getLogger(__name__)


def index_document_task(document_id: int) -> None:
    db = SessionLocal()
    try:
        document = db.get(Document, document_id)
        if not document:
            return

        document.status = "indexing"
        document.updated_at = datetime.utcnow()
        db.commit()

        docs = load_file(document.file_path)
        chunks = split_documents(docs)
        chunk_count = add_chunks(document.user_id, document.id, document.filename, chunks)

        document.status = "indexed"
        document.chunk_count = chunk_count
        document.error_msg = None
        document.updated_at = datetime.utcnow()
        db.commit()
    except Exception as exc:
        logger.exception("document indexing failed document_id=%s", document_id)
        document = db.get(Document, document_id)
        if document:
            document.status = "failed"
            document.error_msg = str(exc)
            document.updated_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()
