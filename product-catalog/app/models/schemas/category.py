from .product import CategoryBase, CategoryCreate, CategoryInDB
from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    parent_category_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryInDB(CategoryBase):
    id: int
    class Config:
        orm_mode = True
