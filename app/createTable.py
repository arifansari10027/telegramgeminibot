# Run once:  python -m app.create_tables
from app.services.database import Base, engine  
from app.models.links import Link               
from app.services.database import MessageLog   

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")
