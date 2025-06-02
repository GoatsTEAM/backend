from pydantic import BaseModel


class AddToCart(BaseModel):
    product_id: str
    quantity: int
    user_id: str