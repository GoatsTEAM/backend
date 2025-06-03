from sqlalchemy.orm import Session
from app.models.product import Product, Category, ProductAttribute
from app.models.schemas.product import ProductCreate, ProductUpdate, CategoryCreate
from typing import List, Optional

def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    if product.attributes:
        for attr in product.attributes:
            db_attr = ProductAttribute(
                name=attr.name,
                value=attr.value,
                product_id=db_product.id
            )
            db.add(db_attr)
        db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    db_product = get_product(db, product_id)
    if db_product is None:
        return None
    for key, value in product.dict(exclude_unset=True).items():
        if key == "attributes":
            continue
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    if product.attributes is not None:
        db.query(ProductAttribute).filter(ProductAttribute.product_id == db_product.id).delete()
        for attr in product.attributes:
            db_attr = ProductAttribute(
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
