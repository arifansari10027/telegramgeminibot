import pytest
from app.handlers.textHandler import register_text_handler


def test_text_handler(dummy_bot, fake_text_message, monkeypatch):
    # Patch Gemini so we don’t hit real API
    monkeypatch.setattr("app.handlers.textHandler.ask_gemini", lambda x: "Hi from Gemini!")

    # Register handler
    register_text_handler(dummy_bot)

    # Manually trigger
    for func, ct, handler in dummy_bot.handlers:
        if "text" in ct and func(fake_text_message):
            handler(fake_text_message)

    # ✅ Verify reply was sent
    assert len(dummy_bot.replies) == 1
    assert dummy_bot.replies[0][1] == "Hi from Gemini!"
