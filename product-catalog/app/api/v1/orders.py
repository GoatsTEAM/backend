from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.services.order_client import get_user_cart, add_to_cart, create_order, get_order
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/cart", tags=["cart"])
async def cart(request: Request, user=Depends(get_current_user)):
    try:
        return await get_user_cart(user["user_id"], request.headers.get("Authorization"))
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.post("/cart/add", tags=["cart"])
async def cart_add(request: Request, user=Depends(get_current_user)):
    data = await request.json()
    try:
        return await add_to_cart(user["user_id"], data["product_id"], data["quantity"], request.headers.get("Authorization"))
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.post("/orders", tags=["orders"])
async def order_create(request: Request, user=Depends(get_current_user)):
    try:
        return await create_order(user["user_id"], request.headers.get("Authorization"))
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.get("/orders/{order_id}", tags=["orders"])
async def order_get(order_id: str, request: Request, user=Depends(get_current_user)):
    try:
        return await get_order(order_id, user["user_id"], request.headers.get("Authorization"))
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(e))
