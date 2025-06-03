from app.db.database import Base
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, BigInteger, DateTime, func
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, index=True)
    seller_id = Column(String, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    category = relationship("Category", back_populates="products")
    media = relationship("Media", back_populates="product", cascade="all, delete-orphan")
