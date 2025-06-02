import jwt
from app.core.config import settings


def verify_token(token: str) -> dict:
    secret, algorithm = settings.JWT_SECRET, settings.JWT_ALGORITHM
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return payload
    except jwt.PyJWTError:
        raise ValueError("Invalid token")
