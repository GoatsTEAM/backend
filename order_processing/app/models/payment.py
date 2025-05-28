from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional
import uuid

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CASH_ON_DELIVERY = "cash_on_delivery"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Уникальный идентификатор платежа"
    )
    order_id: str = Field(..., description="Связанный заказ")
    amount: float = Field(..., gt=0, description="Сумма платежа")
    method: PaymentMethod = Field(..., description="Способ оплаты")
    status: PaymentStatus = Field(
        default=PaymentStatus.PENDING,
        description="Текущий статус"
    )
    transaction_id: Optional[str] = Field(
        None,
        description="Идентификатор транзакции в платежной системе"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Дата создания UTC"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Дата последнего обновления UTC"
    )

    @validator('amount')
    def round_amount(cls, v):
        return round(v, 2)
    
    @validator('transaction_id')
    def validate_transaction_id(cls, v: Optional[str], values: dict) -> Optional[str]:
        if values.get('status') == PaymentStatus.COMPLETED and not v:
            raise ValueError("Transaction ID required for completed payments")
        return v
    

    def mark_as_completed(self, transaction_id: str) -> None:
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Only pending payments can be completed")
        self.status = PaymentStatus.COMPLETED
        self.transaction_id = transaction_id
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_failed(self) -> None:
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Only pending payments can be marked as failed")
        self.status = PaymentStatus.FAILED
        self.updated_at = datetime.now(timezone.utc)

    def refund(self, amount: Optional[float] = None) -> None:
        if self.status not in {PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED}:
            raise ValueError(
                f"Cannot refund payment in status {self.status.value}"
            )
        
        if amount:
            if amount > self.amount:
                raise ValueError("Refund amount exceeds payment amount")
            self.status = PaymentStatus.PARTIALLY_REFUNDED
        else:
            self.status = PaymentStatus.REFUNDED
        
        self.updated_at = datetime.now(timezone.utc)