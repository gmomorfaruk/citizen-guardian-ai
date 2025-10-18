from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime

# ==================
# Document Schemas (defining these first)
# ==================

class Document(BaseModel):
    id: uuid.UUID
    original_filename: str
    content_type: str
    created_at: datetime
    owner_id: uuid.UUID

    class Config:
        from_attributes = True

# ==================
# Item Schemas
# ==================

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: uuid.UUID

    class Config:
        from_attributes = True

# ==================
# User Schemas
# ==================

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=72, 
        description="User password must be between 8 and 72 characters."
    )

class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    items: list[Item] = []
    documents: list[Document] = [] # <-- ADD THIS

    class Config:
        from_attributes = True

# ==================
# Token Schemas
# ==================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None