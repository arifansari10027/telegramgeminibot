# app/services/shortenerService.py
import os
import random
import string
from app.models.links import Link
from app.services.database import SessionLocal

# Your short domain for public links
SHORT_DOMAIN = os.getenv("SHORT_DOMAIN", os.getenv("DOMAIN", "http://localhost:8000")).rstrip("/")

def _generate_unique_code(db, length=6):
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if not db.query(Link).filter_by(short_code=code).first():
            return code

def shorten_url(user_id, original_url):
    db = SessionLocal()
    try:
        code = _generate_unique_code(db)
        link = Link(user_id=user_id, original_url=original_url, short_code=code)
        db.add(link)
        db.commit()
        db.refresh(link)
        return f"{SHORT_DOMAIN}/{code}"
    except Exception as e:
        print(f"[ERROR] shorten_url -> {e}")
        db.rollback()
        return None
    finally:
        db.close()

def get_original_url(short_code):
    db = SessionLocal()
    try:
        return db.query(Link).filter_by(short_code=short_code, deleted=False).first()
    finally:
        db.close()

def get_user_links(user_id):
    db = SessionLocal()
    try:
        return db.query(Link).filter_by(user_id=user_id, deleted=False).all()
    finally:
        db.close()

def delete_link(user_id, link_id):
    db = SessionLocal()
    try:
        link = db.query(Link).filter_by(id=link_id, user_id=user_id).first()
        if link:
            link.deleted = True
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"[DB ERROR] {e}")
        return False
    finally:
        db.close()
