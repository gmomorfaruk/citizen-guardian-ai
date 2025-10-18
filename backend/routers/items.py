from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session # <-- ADD THIS IMPORT
from typing import List

from .. import crud, schemas, models, security, database

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.post("/", response_model=schemas.Item, status_code=201)
def create_user_item(
    item: schemas.ItemCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    items = crud.get_user_items(db, user_id=current_user.id, skip=skip, limit=limit)
    return items