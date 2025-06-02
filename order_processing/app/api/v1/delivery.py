from fastapi import APIRouter, Depends
from app.dependencies.actor import get_actor
from app.services.delivery import DeliveryService
from app.models.actor import Actor
from app.schemas.delivery import EstimateRequest, UpdateAddressRequest

router = APIRouter(prefix="/delivery", tags=["delivery"])

@router.post("/estimate")
def get_estimate(request: EstimateRequest, actor: Actor = Depends(get_actor)):
    return DeliveryService().get_estimate(actor.user_id, request.address_id)

@router.get("/{order_id}/status")
def get_status(order_id: str, actor: Actor = Depends(get_actor)):
    return DeliveryService().get_status(actor.user_id, order_id)

@router.post("/{order_id}")
def create_delivery(order_id: str, actor: Actor = Depends(get_actor)):
    return DeliveryService().create_delivery(actor.user_id, order_id)

@router.post("/{order_id}/cancel")
def cancel_delivery(order_id: str, actor: Actor = Depends(get_actor)):
    return DeliveryService().cancel_delivery(actor.user_id, order_id)

@router.put("/{order_id}/address")
def update_address(order_id: str, request: UpdateAddressRequest, actor: Actor = Depends(get_actor)):
    return DeliveryService().update_address(actor.user_id, order_id, request.address_id)
