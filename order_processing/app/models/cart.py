from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import List
import uuid

class CartStatus(str, Enum):
    ACTIVE = "active"
    CONVERTED_TO_ORDER = "converted"
    ABANDONED = "abandoned"

class CartItem(BaseModel):
    product_id: str = Field(..., description="ID товара из каталога")
    quantity: int = Field(1, gt=0, le=100, description="Количество (1-100 шт)")
    price: float = Field(..., gt=0, description="Цена на момент добавления")

    @validator('price')
    def round_price(cls, v):
        return round(v, 2)

class Cart(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="UUID корзины")
    user_id: str = Field(..., description="ID пользователя")
    items: List[CartItem] = Field(default=[], description="Список товаров")
    status: CartStatus = Field(default=CartStatus.ACTIVE, description="Текущий статус")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата создания UTC")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата обновления UTC")

    def add_item(self, item: CartItem) -> "Cart":
        for existing_item in self.items:
            if existing_item.product_id == item.product_id:
                new_quantity = existing_item.quantity + item.quantity
                if new_quantity > 100:
                    raise ValueError("Maximum quantity exceeded (100 items)")
                existing_item.quantity = new_quantity
                self.updated_at = datetime.now(timezone.utc)
                return self

        self.items.append(item)
        self.updated_at = datetime.now(timezone.utc)
        return self

    def remove_item(self, product_id: str) -> "Cart":
        initial_count = len(self.items)
        self.items = [i for i in self.items if i.product_id != product_id]
        
        if len(self.items) != initial_count:
            self.updated_at = datetime.now(timezone.utc)
        return self

    def clear(self) -> "Cart":
        if self.items:
            self.items = []
            self.updated_at = datetime.now(timezone.utc)
        return self

    @property
    def total(self) -> float:
        return round(sum(item.price * item.quantity for item in self.items), 2)
    
    def mark_as_converted(self) -> None:
        if self.status != CartStatus.ACTIVE:
            raise ValueError("Only active carts can be converted to orders")
        self.status = CartStatus.CONVERTED_TO_ORDER