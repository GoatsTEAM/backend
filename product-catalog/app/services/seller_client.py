import os
import httpx

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")

async def get_seller_info(seller_id: str, token: str = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{AUTH_SERVICE_URL}/api/v1/sellers/{seller_id}", headers=headers)
        resp.raise_for_status()
        return resp.json()
