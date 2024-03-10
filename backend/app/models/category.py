from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, text, BIGINT, Text, Boolean
from sqlalchemy.orm import relationship
from ..db.session import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    budgeted_amount = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    budgeted_limit = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    icon = Column(String(255))
    color_code = Column(String(7))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    user_id = Column(BIGINT, ForeignKey('users.id'))

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")