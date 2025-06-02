from abc import ABC, abstractmethod
from app.services import (
    CartService,
    OrderService,
    PaymentService,
    DeliveryService,
)


class ServicesFactory(ABC):
    @abstractmethod
    def get_cart_service(self) -> CartService:
        pass

    @abstractmethod
    def get_order_service(self) -> OrderService:
        pass

    @abstractmethod
    def get_payment_service(self) -> PaymentService:
        pass

    @abstractmethod
    def get_delivery_service(self) -> DeliveryService:
        pass