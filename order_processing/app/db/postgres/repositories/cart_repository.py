from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres.models.cart_model import Cart as CartModel, CartItem as CartItemModel
from app.models.cart import Cart, CartItem, CartStatus
from app.repositories.abstract_cart_repository import AbstractCartRepository
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

class CartRepository(AbstractCartRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cart(self, cart_id: str) -> Optional[Cart]:
        try:
            result = await self.db.execute(
                select(CartModel)
                .where(CartModel.id == cart_id)
                .options(selectinload(CartModel.items)))
            cart_model = result.scalars().first()
            return self._map_to_domain(cart_model) if cart_model else None
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    async def save_cart(self, cart: Cart) -> None:
        try:
            # Получаем существующую корзину
            result = await self.db.execute(
                select(CartModel)
                .where(CartModel.id == cart.id)
                .options(selectinload(CartModel.items)))
            cart_model = result.scalars().first()
            
            if not cart_model:
                raise ValueError(f"Cart {cart.id} not found")
            
            # Обновление основных полей
            cart_model.status = cart.status.value
            cart_model.updated_at = datetime.now(timezone.utc)
            
            # Удаление старых элементов
            await self.db.execute(delete(CartItemModel).where(CartItemModel.cart_id == cart.id))
            
            # Добавление новых элементов
            for item in cart.items:
                self.db.add(CartItemModel(
                    cart_id=cart.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                ))
            
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        except ValueError as e:
            await self.db.rollback()
            raise

    async def create_cart(self, user_id: str) -> Cart:
        try:
            cart_model = CartModel(
                user_id=user_id,
                status=CartStatus.ACTIVE.value,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.db.add(cart_model)
            await self.db.commit()
            await self.db.refresh(cart_model)
            return self._map_to_domain(cart_model)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    async def get_user_active_cart(self, user_id: str) -> Optional[Cart]:
        try:
            result = await self.db.execute(
                select(CartModel)
                .where(
                    CartModel.user_id == user_id,
                    CartModel.status == CartStatus.ACTIVE.value
                )
                .options(selectinload(CartModel.items)))
            cart_model = result.scalars().first()
            return self._map_to_domain(cart_model) if cart_model else None
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")
    
    async def update_cart_status(self, cart_id: str, status: str) -> None:
        try:
            result = await self.db.execute(
                select(CartModel).where(CartModel.id == cart_id))
            cart_model = result.scalars().first()
            
            if not cart_model:
                raise ValueError(f"Cart {cart_id} not found")
            
            cart_model.status = status
            cart_model.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def _map_to_domain(self, cart_model: CartModel) -> Cart:
        return Cart(
            id=cart_model.id,
            user_id=cart_model.user_id,
            items=[
                CartItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=float(item.price))
                for item in cart_model.items
            ],
            status=CartStatus(cart_model.status),
            created_at=cart_model.created_at.replace(tzinfo=timezone.utc),
            updated_at=cart_model.updated_at.replace(tzinfo=timezone.utc)
        )