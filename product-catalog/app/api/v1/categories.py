from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ... import schemas, crud, database
from typing import List
from app.core.auth import require_roles

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/categories/", response_model=schemas.CategoryInDB, tags=["categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "operator"]))):
    return crud.create_category(db, category)

@router.get("/categories/", response_model=List[schemas.CategoryInDB], tags=["categories"])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "seller", "buyer", "operator"]))):
    return crud.get_categories(db, skip=skip, limit=limit)
