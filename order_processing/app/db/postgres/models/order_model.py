from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Numeric, Enum
from sqlalchemy.orm import relationship
from .base import Base, generate_uuid

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=generate_uuid, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(
        Enum("created", "paid", "shipped", "delivered", "cancelled", 
             name="order_status"),
        nullable=False,
        default="created"
    )
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    payment_id = Column(String, ForeignKey("payments.id"), nullable=True)
    delivery_id = Column(String, ForeignKey("deliveries.id"), nullable=True)
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order")
    delivery = relationship("Delivery", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(String, primary_key=True, default=generate_uuid, nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    order = relationship("Order", back_populates="items")