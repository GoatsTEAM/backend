from fastapi import HTTPException, status
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.models.actor import Actor
from app.repositories.abstract_payment_repository import AbstractPaymentRepository
from typing import Optional

class PaymentService:
    def __init__(self, repo: AbstractPaymentRepository):
        self.repo = repo

    async def create_payment(self,actor: Actor, order_id: str, amount: float, method: PaymentMethod) -> Payment:
        try:
            if not self.actor.is_buyer():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only buyers can create payments"
                )

            payment = Payment(
                order_id=order_id,
                amount=amount,
                method=method
            )
            return await self.repo.create_payment(payment)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create payment: {str(e)}"
            )

    async def process_payment(self, payment_id: str, transaction_id: str) -> Payment:
        try:
            payment = await self.repo.get_payment(payment_id)
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            payment.mark_as_completed(transaction_id)
            await self.repo.update_payment(payment)
            
            # Интеграция с OrderService
            # await order_service.mark_order_as_paid(payment.order_id, payment.id)
            
            return payment
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process payment: {str(e)}"
            )

    async def mark_payment_as_failed(self, payment_id: str) -> Payment:
        try:
            payment = await self.repo.get_payment(payment_id)
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            payment.mark_as_failed()
            await self.repo.update_payment(payment)
            return payment
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to mark payment as failed: {str(e)}"
            )

    async def refund_payment(self,actor: Actor, payment_id: str, amount: Optional[float] = None) -> Payment:
        try:
            if not self.actor.is_moderator():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Refunds require moderator privileges"
                )

            payment = await self.repo.get_payment(payment_id)
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            payment.refund(amount)
            await self.repo.update_payment(payment)
            
            # Интеграция с платежным шлюзом
            # await payment_gateway.refund(payment.transaction_id, amount)
            
            return payment
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to refund payment: {str(e)}"
            )

    async def get_payment_details(self, payment_id: str) -> Payment:
        try:
            payment = await self.repo.get_payment(payment_id)
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            self._validate_access(payment)
            return payment
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get payment details: {str(e)}"
            )

    def _validate_access(self, payment: Payment):
        pass