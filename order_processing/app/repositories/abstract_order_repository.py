from abc import ABC, abstractmethod
from app.models.order import Order, OrderStatus
from typing import List, Optional

class AbstractOrderRepository(ABC):
    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_order(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def update_order(self, order: Order) -> None:
        pass

    @abstractmethod
    async def get_user_orders(self, user_id: str) -> List[Order]:
        pass

    @abstractmethod
    async def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        pass

    @abstractmethod
    async def update_order_status(self, order_id: str, status: OrderStatus) -> None:
        pass