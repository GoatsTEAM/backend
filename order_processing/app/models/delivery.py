from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional
import uuid

class DeliveryMethod(str, Enum):
    COURIER = "courier"
    PICKUP = "pickup"
    POST = "post"

class DeliveryStatus(str, Enum):
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELED = "canceled"

class Delivery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str = Field(..., description="ID связанного заказа")
    method: DeliveryMethod = Field(..., description="Способ доставки")
    status: DeliveryStatus = Field(default=DeliveryStatus.PROCESSING, description="Статус доставки")
    tracking_number: Optional[str] = Field(None, max_length=50, description="Трек-номер")
    address: str = Field(..., min_length=5, description="Адрес доставки")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата создания UTC")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата обновления UTC")

    @validator('address')
    def validate_address(cls, v):
        if not v.strip():
            raise ValueError("Address cannot be empty")
        return v.strip()
    
    def ship(self, tracking_number: str) -> None:
        if self.status != DeliveryStatus.PROCESSING:
            raise ValueError("Only processing deliveries can be shipped")
        self.status = DeliveryStatus.SHIPPED
        self.tracking_number = tracking_number
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_delivered(self) -> None:
        if self.status != DeliveryStatus.SHIPPED:
            raise ValueError("Only shipped deliveries can be marked as delivered")
        self.status = DeliveryStatus.DELIVERED
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_failed(self, reason: str) -> None:
        self.status = DeliveryStatus.FAILED
        self.tracking_number = f"{self.tracking_number or ''} [FAILED: {reason}]"
        self.updated_at = datetime.now(timezone.utc)
    
    def cancel(self) -> None:
        if self.status in (DeliveryStatus.SHIPPED, DeliveryStatus.DELIVERED):
            raise ValueError("Cannot cancel already shipped or delivered delivery")
        self.status = DeliveryStatus.CANCELED
        self.updated_at = datetime.now(timezone.utc)