from sqlalchemy.orm import Session
from typing import Union, Optional
import uuid

from . import models, schemas, security

# (User and Item functions remain the same)
# ==================
# User CRUD Functions
# ==================

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Union[models.User, bool]:
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user

# ==================
# Item CRUD Functions
# ==================

def get_user_items(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[models.Item]:
    return db.query(models.Item).filter(models.Item.owner_id == user_id).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: uuid.UUID) -> models.Item:
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# =======================
# Document CRUD Functions
# =======================

# --- ADD THIS NEW FUNCTION ---
def get_document_by_id(db: Session, document_id: uuid.UUID) -> Optional[models.Document]:
    """
    Retrieves a single document by its ID.
    """
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def create_user_document(db: Session, owner_id: uuid.UUID, original_filename: str, unique_filename: str, content_type: str) -> models.Document:
    db_document = models.Document(
        owner_id=owner_id,
        original_filename=original_filename,
        unique_filename=unique_filename,
        content_type=content_type
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_user_documents(db: Session, user_id: uuid.UUID) -> list[models.Document]:
    return db.query(models.Document).filter(models.Document.owner_id == user_id).all()