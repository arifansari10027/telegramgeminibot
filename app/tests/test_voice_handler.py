import pytest
from app.handlers.voiceHandler import register_voice_handler


def test_voice_handler(dummy_bot, fake_voice_message, monkeypatch):
    # --- Patch AudioSegment.from_file ---
    class FakeAudio:
        def export(self, buf, format):
            buf.write(b"fake wav data")
    monkeypatch.setattr("app.handlers.voiceHandler.AudioSegment.from_file",
                        lambda *a, **k: FakeAudio())

    # --- Patch speech recognition ---
    class DummyRecognizer:
        def record(self, *a, **k): return "fake audio"
        def recognize_google(self, *a, **k): return "hi"
    monkeypatch.setattr("app.handlers.voiceHandler.sr.Recognizer", lambda: DummyRecognizer())

    # Fake AudioFile
    class DummyAudioFile:
        def __enter__(self): return "fake audio file"
        def __exit__(self, *a): pass
    monkeypatch.setattr("app.handlers.voiceHandler.sr.AudioFile", lambda *a, **k: DummyAudioFile())

    # --- Patch Gemini + gTTS ---
    monkeypatch.setattr("app.handlers.voiceHandler.ask_gemini", lambda x: "Hey there!")
    monkeypatch.setattr("app.handlers.voiceHandler.gTTS",
                        lambda text, lang: type("tts", (), {
                            "write_to_fp": lambda self, buf: buf.write(b"voice")
                        })())

    # Register handler
    register_voice_handler(dummy_bot)

    # Manually trigger
    for func, ct, handler in dummy_bot.handlers:
        if "voice" in ct:
            handler(fake_voice_message)

    # ✅ Assert voice was sent
    assert len(dummy_bot.voices) == 1
    assert dummy_bot.voices[0][0] == 123
