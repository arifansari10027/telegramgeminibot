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

from app.services.database import Base, engine
from app.models.links import Link 

from app.services.shortenerService import shorten_url, get_original_url

log = logging.getLogger("uvicorn")
app = FastAPI(title="Telegram Bot + URL Shortener")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
BASE_URL = os.getenv("BASE_URL")  # for webhook
SHORT_DOMAIN = os.getenv("SHORT_DOMAIN")  # for short links
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")  

if not TELEGRAM_TOKEN:
    log.warning("TELEGRAM_TOKEN is not set. Webhook will not be configured.")

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")

register_text_handler(bot)
register_voice_handler(bot)
register_image_handler(bot)
register_url_handler(bot)

@app.on_event("startup")
def _startup():
    Base.metadata.create_all(bind=engine)

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

@app.get("/healthz")
def healthz():
    return {"ok": True}

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

class ShortenRequest(BaseModel):
    user_id: int
    original_url: str

@app.post("/shorten")
def api_shorten(req: ShortenRequest):
    short_url = shorten_url(user_id=req.user_id, original_url=req.original_url)
    if not short_url:
        raise HTTPException(status_code=500, detail="Failed to shorten URL")
    # Always return SHORT_DOMAIN + code
    return {"short_url": f"{SHORT_DOMAIN.rstrip('/')}/{short_url}"}

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    link = get_original_url(short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=link.original_url)
