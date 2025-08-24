import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class MessageLog(Base):
    __tablename_ = "message"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    input_type = Column(String)
    content = Column(Text)
    reply = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)