from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.services.database import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)          
    original_url = Column(Text, nullable=False)
    short_code = Column(String(12), unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
