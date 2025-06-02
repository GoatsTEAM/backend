from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import uuid
from .cart import CartStatus, Cart

class OrderStatus(str, Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: str = Field(..., description="Идентификатор товара из каталога")
    quantity: int = Field(..., gt=0, le=100, description="Количество (1-100 шт)")
    price: float = Field(..., gt=0, description="Цена на момент оформления")

    @validator('price')
    def round_price(cls, v: float) -> float:
        return round(v, 2)

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="UUID заказа")
    user_id: str = Field(..., description="Идентификатор пользователя")
    items: List[OrderItem] = Field(..., min_items=1, description="Список товаров")
    status: OrderStatus = Field(default=OrderStatus.CREATED, description="Текущий статус")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата создания UTC")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата обновления UTC")
    payment_id: Optional[str] = Field(None, description="Идентификатор платежа")
    delivery_id: Optional[str] = Field(None, description="Идентификатор доставки")

    @validator('items')
    def validate_items(cls, v: List[OrderItem]) -> List[OrderItem]:
        if not v:
            raise ValueError("Order must contain at least one item")
        return v

    @classmethod
    def create_from_cart(cls, cart: Cart) -> "Order":
        if not cart.items:
            raise ValueError("Cannot create order from empty cart")
        
        if cart.status != CartStatus.ACTIVE:
            raise ValueError("Only active carts can be converted to orders")

        return cls(
            user_id=cart.user_id,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                ) for item in cart.items
            ]
        )

    def cancel(self) -> "Order":
        if self.status not in (OrderStatus.CREATED, OrderStatus.PAID):
            raise ValueError(f"Cannot cancel order in status {self.status.value}")
        
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)
        return self

    def mark_as_paid(self, payment_id: str) -> None:
        if self.status != OrderStatus.CREATED:
            raise ValueError(f"Cannot pay for order in status {self.status.value}")
        
        self.status = OrderStatus.PAID
        self.payment_id = payment_id
        self.updated_at = datetime.now(timezone.utc)

    @property
    def total_amount(self) -> float:
        return round(sum(item.price * item.quantity for item in self.items), 2)

    def contains_product(self, product_id: str) -> bool:
        return any(item.product_id == product_id for item in self.items)