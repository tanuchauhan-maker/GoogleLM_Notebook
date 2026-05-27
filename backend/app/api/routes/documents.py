from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from pathlib import Path
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user

from app.models.document import Document
from app.models.notebook import Notebook
from app.models.user import User

from app.schemas.document import DocumentCreate, DocumentResponse
from app.utils.document import generate_unique_filename,calculate_file_hash
from app.services.documents.documentUpload import upload_document_file
from app.services.ingestion.prosessDocument import process_document 


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/notebook/{notebook_id}",
    response_model=DocumentResponse
)
async def upload_document(
    notebook_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    
):

    notebook = db.query(Notebook).filter(
        Notebook.id == notebook_id,
        Notebook.user_id == current_user.id
    ).first()

    if not notebook:

        raise HTTPException(
            status_code=404,
            detail="Notebook not found"
        )

    file_content = await file.read()

    upload_data = await upload_document_file(
        user_id=current_user.id,
        notebook_id=notebook_id,
        original_filename=file.filename,
        file_content=file_content,
        content_type=file.content_type
    )

    extension = Path(
        file.filename
    ).suffix

    document = Document(
        notebook_id=notebook_id,
        filename=upload_data["filename"],
        original_filename=file.filename,
        file_extension=extension,
        mime_type=file.content_type,
        file_size=len(file_content),
        storage_path=upload_data["storage_path"],
        content_hash=upload_data["content_hash"],
        processing_status="pending"
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    background_tasks.add_task(
        process_document,
        document_id=document.id   # pass ID, not the ORM object
    )

    return document

@router.get(
    "/notebook/{notebook_id}",
    response_model=list[DocumentResponse]
)
def get_notebook_documents(
    notebook_id: int,
    db: Session = Depends(get_db)
):

    documents = db.query(Document).filter(
        Document.notebook_id == notebook_id
    ).all()

    return documents