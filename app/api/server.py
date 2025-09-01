# app/api/server.py
import os
import logging
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel

import telebot
from telebot.types import Update as TgUpdate

# Handlers
from app.handlers.textHandler import register_text_handler
from app.handlers.voiceHandler import register_voice_handler
from app.handlers.imageHandler import register_image_handler
from app.handlers.urlHandler import register_url_handler

# DB bits (ensure tables exist at startup)
from app.services.database import Base, engine
from app.models.links import Link  # makes sure Link model is imported

# Shortener service
from app.services.shortenerService import shorten_url, get_original_url

log = logging.getLogger("uvicorn")
app = FastAPI(title="Telegram Bot + URL Shortener")

# ── Env ───────────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
BASE_URL = os.getenv("BASE_URL")  # public base (e.g., https://<app>.azurewebsites.net)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")  # optional secret path piece

if not TELEGRAM_TOKEN:
    log.warning("TELEGRAM_TOKEN is not set. Webhook will not be configured.")

# ── Telegram bot (webhook mode) ───────────────────────────────────────────────
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")

# Register your existing handlers on this bot
register_text_handler(bot)
register_voice_handler(bot)
register_image_handler(bot)
register_url_handler(bot)

# ── Models / tables ensure ───────────────────────────────────────────────────
@app.on_event("startup")
def _startup():
    # Ensure tables are created (safe to call repeatedly)
    Base.metadata.create_all(bind=engine)

    # Configure webhook only if we have a public base URL & token
    if TELEGRAM_TOKEN and BASE_URL:
        if WEBHOOK_SECRET:
            path = f"/webhook/{WEBHOOK_SECRET}"
        else:
            path = "/webhook"
        webhook_url = f"{BASE_URL.rstrip('/')}{path}"
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
                data={"url": webhook_url},
                timeout=10
            )
            r.raise_for_status()
            log.info(f"Telegram webhook set to {webhook_url}")
        except Exception as e:
            log.error(f"Failed to set Telegram webhook: {e}")
    else:
        log.warning("BASE_URL or TELEGRAM_TOKEN missing — not setting webhook.")

# ── Health check ─────────────────────────────────────────────────────────────
@app.get("/healthz")
def healthz():
    return {"ok": True}

# ── Webhook endpoint ─────────────────────────────────────────────────────────
# Use secret path if provided
_webhook_path = f"/webhook/{WEBHOOK_SECRET}" if WEBHOOK_SECRET else "/webhook"

@app.post(_webhook_path)
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = TgUpdate.de_json(data)
        bot.process_new_updates([update])
        return JSONResponse({"ok": True})
    except Exception as e:
        log.exception("Webhook error")
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

# ── Shortener API ────────────────────────────────────────────────────────────
class ShortenRequest(BaseModel):
    user_id: int
    original_url: str

@app.post("/shorten")
def api_shorten(req: ShortenRequest):
    short_url = shorten_url(user_id=req.user_id, original_url=req.original_url)
    if not short_url:
        raise HTTPException(status_code=500, detail="Failed to shorten URL")
    return {"short_url": short_url}

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    link = get_original_url(short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=link.original_url)
