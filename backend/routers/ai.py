import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session # <-- ADD THIS IMPORT

from .. import crud, models, database, ai_service, security

router = APIRouter(
    prefix="/ai",
    tags=["AI Coach"]
)

UPLOAD_DIR = Path("backend/uploaded_files")

@router.post("/analyze-document/{document_id}", response_model=dict)
def analyze_document(
    document_id: uuid.UUID,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_document = crud.get_document_by_id(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if db_document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to analyze this document")
    file_path = UPLOAD_DIR / db_document.unique_filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found on server")
    cv_text = ai_service.extract_text_from_pdf(str(file_path))
    analysis_result = ai_service.analyze_cv_with_ai(cv_text)
    return {"analysis": analysis_result}