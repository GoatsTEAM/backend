import os
import httpx

SEARCH_ENGINE_URL = os.getenv("SEARCH_ENGINE_URL", "http://search-engine:8000")

async def search_products(query: str, limit: int = 10, offset: int = 0):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{SEARCH_ENGINE_URL}/api/v1/search",
            params={"q": query, "limit": limit, "offset": offset}
        )
        resp.raise_for_status()
        return resp.json()

async def index_product(product: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{SEARCH_ENGINE_URL}/api/v1/index", json=product)
        resp.raise_for_status()
        return resp.json()
