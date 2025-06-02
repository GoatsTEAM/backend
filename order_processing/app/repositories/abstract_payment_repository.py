from abc import ABC, abstractmethod
from app.models.payment import Payment, PaymentStatus
from typing import List, Optional

class AbstractPaymentRepository(ABC):
    @abstractmethod
    async def create_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def get_payment(self, payment_id: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def update_payment(self, payment: Payment) -> None:
        pass

    @abstractmethod
    async def get_payments_by_order(self, order_id: str) -> List[Payment]:
        pass

    @abstractmethod
    async def get_payments_by_status(self, status: PaymentStatus) -> List[Payment]:
        pass

    @abstractmethod
    async def update_payment_status(self, payment_id: str, status: PaymentStatus) -> None:
        pass