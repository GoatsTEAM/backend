from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryInDB(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProductAttributeBase(BaseModel):
    name: str
    value: str

class ProductAttributeCreate(ProductAttributeBase):
    pass

class ProductAttributeInDB(ProductAttributeBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category_id: Optional[int] = None
    attributes: Optional[List[ProductAttributeCreate]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductInDB(ProductBase):
    id: int
    category: Optional[CategoryInDB] = None
    class Config:
        orm_mode = True
