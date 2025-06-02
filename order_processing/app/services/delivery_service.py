from fastapi import HTTPException, status
from app.models.delivery import Delivery, DeliveryStatus, DeliveryMethod
from app.models.actor import Actor
from app.repositories.abstract_delivery_repository import AbstractDeliveryRepository
from typing import Optional

class DeliveryService:
    def __init__(self, repo: AbstractDeliveryRepository):
        self.repo = repo

    async def create_delivery(self, actor: Actor,order_id: str, method: str, address: str) -> Delivery:
        try:
            if not actor.is_buyer():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only buyers can create deliveries"
                )

            delivery = Delivery(
                order_id=order_id,  
                method= DeliveryMethod(method),
                address=address
            )
            return await self.repo.create_delivery(delivery)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create delivery: {str(e)}"
            )

    async def update_delivery_status(self, actor: Actor,delivery_id: str, new_status: DeliveryStatus) -> Delivery:
        try:
            if not actor.is_moderator():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This action requires moderator privileges"
                )
            
            await self.repo.update_delivery_status(delivery_id, new_status)
            
            delivery = await self.repo.get_delivery(delivery_id)
            if not delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery not found"
                )
            
            if new_status == DeliveryStatus.SHIPPED:
                await self._send_shipping_notification(delivery)
                
            return delivery
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update delivery status: {str(e)}"
            )

    async def add_tracking_number(self,actor: Actor, delivery_id: str, tracking_number: str) -> Delivery:
        try:
            if not actor.is_moderator():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This action requires moderator privileges"
                )
            
            delivery = await self.repo.get_delivery(delivery_id)
            if not delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery not found"
                )
            
            delivery.ship(tracking_number)
            await self.repo.update_delivery(delivery)
            
            return delivery
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add tracking number: {str(e)}"
            )

    async def mark_as_delivered(self,actor: Actor,  delivery_id: str) -> Delivery:
        try:
            if not actor.is_moderator():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This action requires moderator privileges"
                )
            
            delivery = await self.repo.get_delivery(delivery_id)
            if not delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery not found"
                )
            
            delivery.mark_as_delivered()
            await self.repo.update_delivery(delivery)
            
            # Обновление статуса заказа 
            # await order_service.mark_order_as_delivered(delivery.order_id)
            
            return delivery
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to mark delivery as delivered: {str(e)}"
            )
    
    async def cancel_delivery(self, actor: Actor, delivery_id: str) -> Delivery:
        try:
            if not actor.is_moderator():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This action requires moderator privileges"
                )
            
            delivery = await self.repo.get_delivery(delivery_id)
            if not delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery not found"
                )
            
            delivery.cancel()
            await self.repo.update_delivery(delivery)
            
            return delivery
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel delivery: {str(e)}"
            )
