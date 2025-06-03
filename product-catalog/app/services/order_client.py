import os
import httpx

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-processing:8000")

async def get_user_cart(user_id: int, token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORDER_SERVICE_URL}/api/v1/cart/", headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        return resp.json()

async def add_to_cart(user_id: int, product_id: str, quantity: int, token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{ORDER_SERVICE_URL}/api/v1/cart/add",
            json={"product_id": product_id, "quantity": quantity},
            headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        return resp.json()

async def create_order(user_id: int, token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{ORDER_SERVICE_URL}/api/v1/orders/", headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        return resp.json()

async def get_order(order_id: str, user_id: int, token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORDER_SERVICE_URL}/api/v1/orders/{order_id}", headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        return resp.json()
