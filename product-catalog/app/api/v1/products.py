from fastapi import APIRouter, Depends, HTTPException
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

@router.post("/products/", response_model=schemas.ProductInDB, tags=["products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "seller"]))):
    return crud.create_product(db, product)

@router.get("/products/", response_model=List[schemas.ProductInDB], tags=["products"])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "seller", "buyer", "operator"]))):
    return crud.get_products(db, skip=skip, limit=limit)

@router.get("/products/{product_id}", response_model=schemas.ProductInDB, tags=["products"])
def read_product(product_id: int, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "seller", "buyer", "operator"]))):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=schemas.ProductInDB, tags=["products"])
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "seller"]))):
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", tags=["products"])
def delete_product(product_id: int, db: Session = Depends(get_db), user=Depends(require_roles(["admin"]))):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}
