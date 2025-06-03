from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.services.comments_client import get_product_reviews, add_product_review
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/products/{product_id}/reviews", tags=["reviews"])
async def product_reviews(product_id: int):
    try:
        return await get_product_reviews(product_id)
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.post("/products/{product_id}/reviews", tags=["reviews"])
async def create_review(product_id: int, request: Request, user=Depends(get_current_user)):
    review = await request.json()
    try:
        return await add_product_review(product_id, user["user_id"], review, request.headers.get("Authorization"))
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(e))
