from redis.asyncio import Redis
from app.models.cart import Cart
from app.repositories.abstract_cart_repository import AbstractCartRepository
from typing import Optional
import json

CART_TTL_SECONDS = 60 * 60 * 24

class RedisCartRepository(AbstractCartRepository):
    def __init__(self, redis: Redis):
        self.redis = redis

    def _cart_key(self, cart_id: str) -> str:
        return f"cart:{cart_id}"

    def _user_active_cart_key(self, user_id: str) -> str:
        return f"user_active_cart:{user_id}"

    async def get_cart(self, cart_id: str) -> Optional[Cart]:
        key = self._cart_key(cart_id)
        raw = await self.redis.get(key)
        if raw is None:
            return None
        data = json.loads(raw)
        return Cart.model_validate(data)

    async def save_cart(self, cart: Cart) -> None:
        key = self._cart_key(cart.id)
        user_key = self._user_active_cart_key(cart.user_id)
        raw = cart.model_dump_json()
        await self.redis.set(key, raw, ex=CART_TTL_SECONDS)
        await self.redis.set(user_key, cart.id, ex=CART_TTL_SECONDS)

    async def create_cart(self, user_id: str) -> Cart:
        existing = await self.get_user_active_cart(user_id)
        if existing:
            return existing

        cart = Cart(user_id=user_id)
        await self.save_cart(cart)
        return cart

    async def get_user_active_cart(self, user_id: str) -> Optional[Cart]:
        user_key = self._user_active_cart_key(user_id)
        cart_id = await self.redis.get(user_key)
        if not cart_id:
            return None
        return await self.get_cart(cart_id.decode())
