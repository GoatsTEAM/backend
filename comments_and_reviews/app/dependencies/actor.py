from app.core.security import verify_token
from app.models.actor import Actor


def get_actor(token: str) -> Actor:
    payload = verify_token(token)
    actor = Actor.from_jwt(payload)
    return actor
