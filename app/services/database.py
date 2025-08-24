import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import Base

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the MessageLog table
class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    message_type = Column(String, nullable=False)   # text / voice / image
    content = Column(Text, nullable=False)          # actual text, transcript, or description
    created_at = Column(DateTime, default=datetime.utcnow)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)


# Helper function to save messages
def save_message(user_id: str, message_type: str, content: str):
    session = SessionLocal()
    try:
        log = MessageLog(user_id=user_id, message_type=message_type, content=content)
        session.add(log)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[DB ERROR] {e}")
    finally:
        session.close()