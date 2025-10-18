import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session # <-- ADD THIS IMPORT
from typing import List

from .. import crud, schemas, models, database, security

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("backend/uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload", response_model=schemas.Document, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    unique_id = uuid.uuid4()
    file_extension = Path(file.filename).suffix
    unique_filename = f"{unique_id}{file_extension}"
    file_location = UPLOAD_DIR / unique_filename
    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    db_document = crud.create_user_document(
        db=db,
        owner_id=current_user.id,
        original_filename=file.filename,
        unique_filename=unique_filename,
        content_type=file.content_type
    )
    return db_document

@router.get("/", response_model=List[schemas.Document])
def read_own_documents(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.get_user_documents(db=db, user_id=current_user.id)

@router.get("/{document_id}/download")
def download_document(
    document_id: uuid.UUID,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_document = crud.get_document_by_id(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if db_document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to download this document")
    file_path = UPLOAD_DIR / db_document.unique_filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(path=file_path, filename=db_document.original_filename, media_type=db_document.content_type)