from redis.asyncio import Redis

from app.db import (
    DeliveryRepository,
    OrderRepository,
    PaymentRepository,
    RedisCartRepository,
)

from app.services import (
    CartService,
    OrderService,
    DeliveryService,
    PaymentService,
    ServicesFactory,
)


class ServicesFactoryImpl(ServicesFactory):
    def __init__(self, redis: Redis):
        self.cart_repo = RedisCartRepository(redis)
        self.order_repo = OrderRepository()
        self.pay_repo = PaymentRepository()
        self.del_repo = DeliveryRepository()
        self.cart_serv = CartService()

    def get_cart_service(self) -> CartService:
        return CartService(self.cart_repo)

    def get_order_service(self) -> OrderService:
        return OrderService(self.order_repo, self.get_cart_service())

    def get_payment_service(self) -> PaymentService:
        return PaymentService(self.pay_repo)
    
    def get_delivery_service(self) -> DeliveryService:
        return DeliveryService(self.del_repo)


def get_services_factory() -> ServicesFactory:
    from app.db import init_redis

    redis = init_redis()
    return ServicesFactoryImpl(redis)