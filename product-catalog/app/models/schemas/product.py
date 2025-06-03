from pydantic import BaseModel
from typing import Optional, List, Dict
from .media import MediaInDB

class CategoryBase(BaseModel):
    name: str
    parent_category_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryInDB(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    seller_id: str
    media: Optional[List[MediaInDB]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductInDB(ProductBase):
    id: int
    category: Optional[CategoryInDB] = None
    class Config:
        orm_mode = True
