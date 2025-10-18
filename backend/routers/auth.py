from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session # <-- ADD THIS IMPORT
import os

from .. import database, schemas, crud, security

router = APIRouter(tags=['Authentication'])

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, email=user_credentials.username, password=user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = security.create_access_token(
        data={"user_id": str(user.id), "email": user.email},
        expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}