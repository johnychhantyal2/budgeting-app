from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Date, Text, TIMESTAMP, text, BIGINT, Boolean
from sqlalchemy.orm import relationship
from ..db.session import Base  # Make sure this import path is correct based on your project structure

class Transaction(Base):
    __tablename__ = "transactions"

    TransactionID = Column(BIGINT, primary_key=True, autoincrement=True)
    CategoryID = Column(BIGINT, ForeignKey('categories.id',ondelete="SET NULL"), nullable=True)  # Match the case to your DB schema
    UserID = Column(BIGINT, ForeignKey('users.id'), nullable=False)  # Match the case to your DB schema
    Amount = Column(DECIMAL(10, 2), nullable=False)
    Date = Column(Date, nullable=False)
    Description = Column(String(255))
    Note = Column(Text)
    Location = Column(String(255))
    CreatedAt = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    UpdatedAt = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    Is_Income = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
