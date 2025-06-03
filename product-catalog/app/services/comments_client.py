import os
import httpx

COMMENTS_SERVICE_URL = os.getenv("COMMENTS_SERVICE_URL", "http://comments-and-reviews:8000")

async def get_product_reviews(product_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{COMMENTS_SERVICE_URL}/api/v1/reviews/{product_id}")
        resp.raise_for_status()
        return resp.json()

async def add_product_review(product_id: int, user_id: int, review: dict, token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{COMMENTS_SERVICE_URL}/api/v1/reviews/{product_id}",
            json=review,
            headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        return resp.json()
