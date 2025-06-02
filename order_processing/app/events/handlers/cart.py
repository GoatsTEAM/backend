from app.services import ServicesFactory
from app.events.schemas.cart import AddToCart
from app.models.actor import Actor
from app.events.router import Router
from app.events.schemas.event import EventType

cart_router = Router()


@cart_router.add(EventType.ADD_TO_CART, AddToCart)
async def handle_add_to_cart(body: AddToCart, services: ServicesFactory):
    actor = Actor(user_id=body.user_id, roles=["user"])  # или заглушка
    cart_service = services.get_cart_service()
    await cart_service.add_item(actor, product_id=body.product_id, quantity=body.quantity)
    return {"status": "ok"}