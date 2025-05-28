from abc import ABC, abstractmethod
from app.models.cart import Cart
from typing import Optional

class AbstractCartRepository(ABC):
    @abstractmethod
    async def get_cart(self, cart_id: str) -> Optional[Cart]:
        pass

    @abstractmethod
    async def save_cart(self, cart: Cart) -> None:
        pass

    @abstractmethod
    async def create_cart(self, user_id: str) -> Cart:
        pass

    @abstractmethod
    async def get_user_active_cart(self, user_id: str) -> Optional[Cart]:
        pass

    @abstractmethod
    async def update_cart_status(self, cart_id: str, status: str) -> None:
        pass