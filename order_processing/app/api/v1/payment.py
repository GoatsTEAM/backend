from fastapi import APIRouter, Depends
from app.dependencies.actor import get_actor
from app.services import PaymentService
from app.models.actor import Actor
from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    order_id: str

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/")
def create_payment(request: CreatePaymentRequest, actor: Actor = Depends(get_actor)):
    return PaymentService().create_payment(actor.user_id, request.order_id, request.method)

@router.get("/{payment_id}")
def get_payment(payment_id: str, actor: Actor = Depends(get_actor)):
    return PaymentService().get_payment(actor.user_id, payment_id)

@router.get("/{payment_id}/status")
def get_status(payment_id: str, actor: Actor = Depends(get_actor)):
    return PaymentService().get_status(actor.user_id, payment_id)

@router.post("/{payment_id}/confirm")
def confirm_payment(payment_id: str, actor: Actor = Depends(get_actor)):
    return PaymentService().confirm_payment(actor.user_id, payment_id)

@router.post("/{payment_id}/cancel")
def cancel_payment(payment_id: str, actor: Actor = Depends(get_actor)):
    return PaymentService().cancel_payment(actor.user_id, payment_id)

@router.get("/")
def list_payments(actor: Actor = Depends(get_actor)):
    return PaymentService().list_payments(actor.user_id)