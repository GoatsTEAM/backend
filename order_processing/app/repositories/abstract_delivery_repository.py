from abc import ABC, abstractmethod
from app.models.delivery import Delivery, DeliveryStatus
from typing import List, Optional

class AbstractDeliveryRepository(ABC):
    @abstractmethod
    async def create_delivery(self, delivery: Delivery) -> Delivery:
        pass

    @abstractmethod
    async def get_delivery(self, delivery_id: str) -> Optional[Delivery]:
        pass

    @abstractmethod
    async def update_delivery(self, delivery: Delivery) -> None:
        pass

    @abstractmethod
    async def get_deliveries_by_status(self, status: DeliveryStatus) -> List[Delivery]:
        pass

    @abstractmethod
    async def get_deliveries_by_order(self, order_id: str) -> List[Delivery]:
        pass

    @abstractmethod
    async def update_delivery_status(self, delivery_id: str, status: DeliveryStatus) -> None:
        pass