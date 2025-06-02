from fastapi import APIRouter, Depends
from app.dependencies.actor import get_actor
from app.services import OrderService
from app.models.actor import Actor

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/")
def create_order(actor: Actor = Depends(get_actor)):
    return OrderService().create_order(actor.user_id)

@router.get("/{order_id}")
def get_order(order_id: str, actor: Actor = Depends(get_actor)):
    return OrderService().get_order(actor.user_id, order_id)

@router.get("/")
def list_orders(actor: Actor = Depends(get_actor)):
    return OrderService().list_orders(actor.user_id)

@router.post("/{order_id}/cancel")
def cancel_order(order_id: str, actor: Actor = Depends(get_actor)):
    return OrderService().cancel_order(actor.user_id, order_id)

@router.get("/{order_id}/status")
def get_status(order_id: str, actor: Actor = Depends(get_actor)):
    return OrderService().get_status(actor.user_id, order_id)