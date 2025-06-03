import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import httpx

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
JWT_SECRET = os.getenv("JWT_SECRET", "secret")
bearer_scheme = HTTPBearer()

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: int = payload["user_id"]
    except (JWTError, KeyError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{AUTH_SERVICE_URL}/users/{user_id}", headers={"Authorization": f"Bearer {token}"})
        if resp.status_code != 200:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or unauthorized")
        user_data = resp.json()
        if user_data.get("is_banned"):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "User is banned")
    return user_data

from typing import List

def require_roles(roles: List[str]):
    def dependency(user = Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
        return user
    return dependency
