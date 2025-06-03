from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Add attributes if any
    if product.attributes:
        for attr in product.attributes:
            db_attr = models.ProductAttribute(
                name=attr.name,
                value=attr.value,
                product_id=db_product.id
            )
            db.add(db_attr)
        db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate) -> Optional[models.Product]:
    db_product = get_product(db, product_id)
    if db_product is None:
        return None
    for key, value in product.dict(exclude_unset=True).items():
        if key == "attributes":
            continue  # handle attributes separately
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    # Update attributes if provided
    if product.attributes is not None:
        db.query(models.ProductAttribute).filter(models.ProductAttribute.product_id == db_product.id).delete()
        for attr in product.attributes:
            db_attr = models.ProductAttribute(
                name=attr.name,
                value=attr.value,
                product_id=db_product.id
            )
            db.add(db_attr)
        db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if db_product is None:
        return False
    db.delete(db_product)
    db.commit()
    return True
