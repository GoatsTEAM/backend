from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Enum
from sqlalchemy.orm import relationship
from .base import Base, generate_uuid

class Delivery(Base):
    __tablename__ = "deliveries"
    
    id = Column(String, primary_key=True, default=generate_uuid, nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    method = Column(
        Enum("courier", "pickup", "post", name="delivery_method"),
        nullable=False
    )
    status = Column(
        Enum("preparing", "shipped", "delivered", name="delivery_status"),
        nullable=False,
        default="preparing"
    )
    address = Column(String, nullable=False)
    tracking_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    order = relationship("Order", back_populates="delivery")