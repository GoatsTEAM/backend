from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Numeric
from sqlalchemy.orm import relationship
from .base import Base, generate_uuid

class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(String, primary_key=True, default=generate_uuid, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(String, primary_key=True, default=generate_uuid, nullable=False)
    cart_id = Column(String, ForeignKey("carts.id"), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)
    cart = relationship("Cart", back_populates="items")