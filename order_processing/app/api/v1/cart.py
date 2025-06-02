from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.dependencies.actor import get_actor_from_token
from app.models.actor import Actor
from app.services.cart_service import CartService

router = APIRouter()

cart_service = CartService()


class AddItemRequest(BaseModel):
    product_id: str
    quantity: int


@router.get("/", summary="Получить корзину")
async def get_cart(actor: Actor = Depends(get_actor_from_token)):
    return await cart_service.get_cart(actor.id)


@router.post("/add", summary="Добавить товар в корзину")
async def add_item(req: AddItemRequest, actor: Actor = Depends(get_actor_from_token)):
    await cart_service.add_item(actor.id, req.product_id, req.quantity)
    return {"status": "ok"}


@router.delete("/remove/{product_id}", summary="Удалить товар из корзины")
async def remove_item(product_id: str, actor: Actor = Depends(get_actor_from_token)):
    await cart_service.remove_item(actor.id, product_id)
    return {"status": "ok"}


@router.delete("/clear", summary="Очистить корзину")
async def clear_cart(actor: Actor = Depends(get_actor_from_token)):
    await cart_service.clear_cart(actor.id)
    return {"status": "ok"}