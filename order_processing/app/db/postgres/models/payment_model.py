from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Numeric, Enum
from sqlalchemy.orm import relationship
from .base import Base, generate_uuid

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String, primary_key=True, default=generate_uuid, nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    method = Column(
        Enum("card", "cash", "apple_pay", "google_pay", name="payment_method"),
        nullable=False
    )
    status = Column(
        Enum("pending", "paid", "failed", "refunded", name="payment_status"),
        nullable=False,
        default="pending"
    )
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    order = relationship("Order", back_populates="payment")