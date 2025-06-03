from fastapi import APIRouter, HTTPException, status, Query
from app.services.search_client import search_products

router = APIRouter()

@router.get("/search", tags=["search"])
async def search(q: str = Query(..., description="Search query"), limit: int = 10, offset: int = 0):
    try:
        return await search_products(q, limit, offset)
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(e))
