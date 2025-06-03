from app.db.database import Base
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, SmallInteger, JSON, CheckConstraint
from sqlalchemy.orm import relationship

class Media(Base):
    __tablename__ = "media"
    media_id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    storage_key = Column(String(500), nullable=False)
    media_type = Column(String(10), nullable=False)
    position = Column(SmallInteger, default=0)
    metadata = Column(JSON)
    product = relationship("Product", back_populates="media")
    __table_args__ = (
        CheckConstraint("media_type IN ('image', 'video')", name="media_type_check"),
    )
