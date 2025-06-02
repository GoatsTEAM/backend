from fastapi import HTTPException, status
from app.models.order import Order, OrderStatus
from app.models.actor import Actor
from app.repositories.abstract_order_repository import AbstractOrderRepository
from app.services.cart_service import CartService


class OrderService:
    def __init__(self, 
        order_repo: AbstractOrderRepository,
        cart_service: CartService,
    ):
        self.order_repo = order_repo
        self.cart_service = cart_service

    async def create_order_from_cart(self, actor: Actor) -> Order:
        try:
            if not self.actor.is_buyer():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only buyers can create orders"
                )

            cart = await self.cart_service.get_or_create_active_cart(actor)
            
            order = Order.create_from_cart(cart)
            
            created_order = await self.order_repo.create_order(order)
            
            await self.cart_service.convert_cart_to_order(cart.id)
            
            return created_order
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create order: {str(e)}"
            )

    async def cancel_order(self,actor: Actor, order_id: str) -> Order:
        try:
            order = await self.order_repo.get_order(order_id)
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            self._validate_ownership(order, actor)
            
            was_paid = order.status == OrderStatus.PAID
            order.cancel()
            await self.order_repo.update_order(order)
            if was_paid:
                await self._initiate_refund(order)
                
            return order
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel order: {str(e)}"
            )

    async def update_order_status(self,actor:Actor,  order_id: str, new_status: OrderStatus) -> Order:
        try:
            if not self.actor.is_moderator():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This action requires moderator privileges"
                )
            
            order = await self.order_repo.get_order(order_id)
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            await self.order_repo.update_order_status(order.id, new_status)
            
            if new_status == OrderStatus.SHIPPED:
                await self._send_shipping_notification(order)
                
            return await self.order_repo.get_order(order_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update order status: {str(e)}"
            )

    async def mark_order_as_paid(self, order_id: str, payment_id: str) -> Order:
        try:
            order = await self.order_repo.get_order(order_id)
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            order.mark_as_paid(payment_id)
            
            await self.order_repo.update_order(order)
            
            return order
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to mark order as paid: {str(e)}"
            )

    def _validate_ownership(self, order: Order, actor: Actor):
        if order.user_id != self.actor.id and not self.actor.is_moderator():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this order"
            )

    async def _initiate_refund(self, order: Order):
        """Интеграция с платежным сервисом"""
        pass
