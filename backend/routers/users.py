from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session # <-- ADD THIS IMPORT
from typing import List

from .. import crud, schemas, database, models, security

router = APIRouter()

@router.post("/register", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user