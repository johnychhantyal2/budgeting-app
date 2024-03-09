from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..db.session import Base 

class BlocklistedToken(Base):
    __tablename__ = "blocklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, index=True)

    def __init__(self, token: str, expires_at: datetime):
        self.token = token
        self.expires_at = expires_at