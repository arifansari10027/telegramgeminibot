import os
import random
import string
from typing import Optional
from app.models.links import Link
from app.services.database import SessionLocal

DOMAIN = os.getenv("SHORT_DOMAIN", "http://localhost:8000")

def _generate_unique_code(db, length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(alphabet, k=length))
        exists = db.query(Link).filter_by(short_code=code).first()
        if not exists:
            return code

def shorten_url(user_id: int, original_url: str) -> Optional[str]:
    db = SessionLocal()
    try:
        code = _generate_unique_code(db)
        link = Link(
            user_id=str(user_id),
            original_url=original_url.strip(),
            short_code=code,
        )
        db.add(link)
        db.commit()
        return f"{DOMAIN}/{code}"
    except Exception as e:
        db.rollback()
        print(f"[ERROR] shorten_url -> {e}")
        return None
    finally:
        db.close()

def get_original_url(short_code: str) -> Optional[Link]:
    db = SessionLocal()
    try:
        return db.query(Link).filter_by(short_code=short_code, deleted=False).first()
    finally:
        db.close()

def increment_click(short_code: str) -> None:
    db = SessionLocal()
    try:
        link = db.query(Link).filter_by(short_code=short_code, deleted=False).first()
        if link:
            link.clicks = (link.clicks or 0) + 1
            db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def get_user_links(user_id: int):
    db = SessionLocal()
    try:
        return db.query(Link).filter_by(user_id=str(user_id), deleted=False).order_by(Link.id.desc()).all()
    finally:
        db.close()

def delete_link(user_id: int, link_id: int) -> bool:
    db = SessionLocal()
    try:
        link = db.query(Link).filter_by(id=link_id, user_id=str(user_id)).first()
        if not link:
            return False
        link.deleted = True
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()
