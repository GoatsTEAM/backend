from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres.models.order_model import Order as OrderModel, OrderItem as OrderItemModel
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.abstract_order_repository import AbstractOrderRepository
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import uuid

class OrderRepository(AbstractOrderRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order: Order) -> Order:
        try:
            order_model = OrderModel(
                id=order.id,
                user_id=order.user_id,
                status=order.status.value,
                total_amount=order.total_amount,
                payment_id=order.payment_id,
                delivery_id=order.delivery_id,
                created_at=order.created_at,
                updated_at=order.updated_at
            )
            
            for item in order.items:
                item_model = OrderItemModel(
                    id=str(uuid.uuid4()),
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                )
                order_model.items.append(item_model)
            
            self.db.add(order_model)
            await self.db.commit()
            await self.db.refresh(order_model)
            return self._map_to_domain(order_model)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    async def get_order(self, order_id: str) -> Optional[Order]:
        try:
            result = await self.db.execute(
                select(OrderModel)
                .where(OrderModel.id == order_id)
                .options(selectinload(OrderModel.items)))
            order_model = result.scalars().first()
            return self._map_to_domain(order_model) if order_model else None
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    async def update_order(self, order: Order) -> None:
        try:
            result = await self.db.execute(
                select(OrderModel)
                .where(OrderModel.id == order.id)
                .options(selectinload(OrderModel.items)))
            order_model = result.scalars().first()
            
            if not order_model:
                raise ValueError(f"Order {order.id} not found")
            
            order_model.status = order.status.value
            order_model.payment_id = order.payment_id
            order_model.delivery_id = order.delivery_id
            order_model.updated_at = datetime.now(timezone.utc)
            
            await self.db.execute(delete(OrderItemModel).where(OrderItemModel.order_id == order.id))
            
            for item in order.items:
                self.db.add(OrderItemModel(
                    order_id=order.id,
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

    async def get_user_orders(self, user_id: str) -> List[Order]:
        try:
            result = await self.db.execute(
                select(OrderModel)
                .where(OrderModel.user_id == user_id)
                .options(selectinload(OrderModel.items)))
            orders = result.scalars().all()
            return [self._map_to_domain(o) for o in orders]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    async def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        try:
            result = await self.db.execute(
                select(OrderModel)
                .where(OrderModel.status == status.value)
                .options(selectinload(OrderModel.items)))
            orders = result.scalars().all()
            return [self._map_to_domain(o) for o in orders]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")
    
    async def update_order_status(self, order_id: str, status: OrderStatus) -> None:
        try:
            result = await self.db.execute(
                select(OrderModel).where(OrderModel.id == order_id))
            order_model = result.scalars().first()
            
            if not order_model:
                raise ValueError(f"Order {order_id} not found")
            
            order_model.status = status.value
            order_model.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def _map_to_domain(self, order_model: OrderModel) -> Order:
        return Order(
            id=order_model.id,
            user_id=order_model.user_id,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=float(item.price)
                ) for item in order_model.items
            ],
            status=OrderStatus(order_model.status),
            payment_id=order_model.payment_id,
            delivery_id=order_model.delivery_id,
            created_at=order_model.created_at.replace(tzinfo=timezone.utc),
            updated_at=order_model.updated_at.replace(tzinfo=timezone.utc)
        )