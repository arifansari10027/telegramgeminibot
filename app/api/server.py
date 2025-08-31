from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from app.services.shortenerService import shorten_url, get_original_url, increment_click

app = FastAPI(title="URL Shortener API")

class ShortenRequest(BaseModel):
    user_id: int
    original_url: HttpUrl 

class ShortenResponse(BaseModel):
    short_url: Optional[str]

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/shorten", response_model=ShortenResponse)
def create_short_url(req: ShortenRequest):
    short_url = shorten_url(user_id=req.user_id, original_url=str(req.original_url))
    if not short_url:
        
        
        return ShortenResponse(short_url=None)
    return ShortenResponse(short_url=short_url)

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    link = get_original_url(short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short URL not found")
    increment_click(short_code)
    return RedirectResponse(url=link.original_url)
