from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres.models.payment_model import Payment as PaymentModel
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.repositories.abstract_payment_repository import AbstractPaymentRepository
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime, timezone

class PaymentRepository(AbstractPaymentRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: Payment) -> Payment:
        try:
            payment_model = PaymentModel(
                id=payment.id,
                order_id=payment.order_id,
                amount=payment.amount,
                method=payment.method.value,
                status=payment.status.value,
                transaction_id=payment.transaction_id,
                created_at=payment.created_at,
                updated_at=payment.updated_at
            )
            self.db.add(payment_model)
            await self.db.commit()
            await self.db.refresh(payment_model)
            return self._map_to_domain(payment_model)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    async def get_payment(self, payment_id: str) -> Optional[Payment]:
        try:
            result = await self.db.execute(
                select(PaymentModel).where(PaymentModel.id == payment_id))
            payment_model = result.scalars().first()
            return self._map_to_domain(payment_model) if payment_model else None
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    async def update_payment(self, payment: Payment) -> None:
        try:
            result = await self.db.execute(
                select(PaymentModel).where(PaymentModel.id == payment.id))
            payment_model = result.scalars().first()
            
            if not payment_model:
                raise ValueError(f"Payment {payment.id} not found")
            
            payment_model.status = payment.status.value
            payment_model.transaction_id = payment.transaction_id
            payment_model.updated_at = datetime.now(timezone.utc)

            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        except ValueError as e:
            raise

    async def get_payments_by_order(self, order_id: str) -> List[Payment]:
        try:
            result = await self.db.execute(
                select(PaymentModel).where(PaymentModel.order_id == order_id))
            payments = result.scalars().all()
            return [self._map_to_domain(p) for p in payments]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    async def get_payments_by_status(self, status: PaymentStatus) -> List[Payment]:
        try:
            result = await self.db.execute(
                select(PaymentModel).where(PaymentModel.status == status.value))
            payments = result.scalars().all()
            return [self._map_to_domain(p) for p in payments]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")
    
    async def update_payment_status(self, payment_id: str, status: PaymentStatus) -> None:
        try:
            result = await self.db.execute(
                select(PaymentModel).where(PaymentModel.id == payment_id))
            payment_model = result.scalars().first()
            
            if not payment_model:
                raise ValueError(f"Payment {payment_id} not found")
            
            payment_model.status = status.value
            payment_model.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def _map_to_domain(self, payment_model: PaymentModel) -> Payment:
        return Payment(
            id=payment_model.id,
            order_id=payment_model.order_id,
            amount=float(payment_model.amount),
            method=PaymentMethod(payment_model.method),
            status=PaymentStatus(payment_model.status),
            transaction_id=payment_model.transaction_id,
            created_at=payment_model.created_at.replace(tzinfo=timezone.utc),
            updated_at=payment_model.updated_at.replace(tzinfo=timezone.utc) if payment_model.updated_at else None
        )