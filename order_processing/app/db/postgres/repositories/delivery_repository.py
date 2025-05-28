from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres.models.delivery_model import Delivery as DeliveryModel
from app.models.delivery import Delivery, DeliveryStatus, DeliveryMethod
from app.repositories.abstract_delivery_repository import AbstractDeliveryRepository
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime, timezone

class DeliveryRepository(AbstractDeliveryRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_delivery(self, delivery: Delivery) -> Delivery:
        try:
            delivery_model = DeliveryModel(
                id=delivery.id,
                order_id=delivery.order_id,
                method=delivery.method.value,
                status=delivery.status.value,
                tracking_number=delivery.tracking_number,
                address=delivery.address,
                created_at=delivery.created_at,
                updated_at=delivery.updated_at
            )
            self.db.add(delivery_model)
            await self.db.commit()
            await self.db.refresh(delivery_model)
            return self._map_to_domain(delivery_model)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    async def get_delivery(self, delivery_id: str) -> Optional[Delivery]:
        try:
            result = await self.db.execute(
                select(DeliveryModel).where(DeliveryModel.id == delivery_id))
            delivery_model = result.scalars().first()
            return self._map_to_domain(delivery_model) if delivery_model else None
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    async def update_delivery(self, delivery: Delivery) -> None:
        try:
            result = await self.db.execute(
                select(DeliveryModel).where(DeliveryModel.id == delivery.id))
            delivery_model = result.scalars().first()
            
            if not delivery_model:
                raise ValueError(f"Delivery {delivery.id} not found")
            
            delivery_model.status = delivery.status.value
            delivery_model.tracking_number = delivery.tracking_number
            delivery_model.updated_at = datetime.now(timezone.utc)
            
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        except ValueError as e:
            await self.db.rollback()
            raise

    async def get_deliveries_by_status(self, status: DeliveryStatus) -> List[Delivery]:
        try:
            result = await self.db.execute(
                select(DeliveryModel).where(DeliveryModel.status == status.value))
            deliveries = result.scalars().all()
            return [self._map_to_domain(d) for d in deliveries]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    async def get_deliveries_by_order(self, order_id: str) -> List[Delivery]:
        try:
            result = await self.db.execute(
                select(DeliveryModel).where(DeliveryModel.order_id == order_id))
            deliveries = result.scalars().all()
            return [self._map_to_domain(d) for d in deliveries]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")
    
    async def update_delivery_status(self, delivery_id: str, status: DeliveryStatus) -> None:
        try:
            result = await self.db.execute(
                select(DeliveryModel).where(DeliveryModel.id == delivery_id))
            delivery_model = result.scalars().first()
            
            if not delivery_model:
                raise ValueError(f"Delivery {delivery_id} not found")
            
            delivery_model.status = status.value
            delivery_model.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def _map_to_domain(self, model: DeliveryModel) -> Delivery:
        return Delivery(
            id=model.id,
            order_id=model.order_id,
            method=DeliveryMethod(model.method),
            status=DeliveryStatus(model.status),
            tracking_number=model.tracking_number,
            address=model.address,
            created_at=model.created_at.replace(tzinfo=timezone.utc),
            updated_at=model.updated_at.replace(tzinfo=timezone.utc) if model.updated_at else None
        )