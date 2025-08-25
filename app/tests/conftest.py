import pytest
from types import SimpleNamespace


# --- DummyBot (shared for all tests) ---
class DummyBot:
    def __init__(self):
        self.handlers = []
        self.replies = []
        self.voices = []

    def message_handler(self, func=None, content_types=None):
        """Mimic TeleBot.message_handler decorator."""
        def decorator(handler_func):
            self.handlers.append((func, content_types or ["text"], handler_func))
            return handler_func
        return decorator

    def reply_to(self, message, text):
        self.replies.append((getattr(message, "text", None), text))

    def send_voice(self, chat_id, voice):
        self.voices.append((chat_id, voice))

    def get_file(self, file_id):
        return type("File", (), {"file_path": "dummy.ogg"})()

    def download_file(self, file_path):
        return b"fake ogg data"


# --- Fixtures ---
@pytest.fixture
def dummy_bot():
    return DummyBot()


@pytest.fixture
def fake_text_message():
    """Simulates a Telegram text message"""
    return SimpleNamespace(
        message_id=1,
        from_user=SimpleNamespace(id=1, username="TestUser"),
        chat=SimpleNamespace(id=1, type="private"),
        text="Hello, world!"
    )


@pytest.fixture
def fake_voice_message():
    """Simulates a Telegram voice message"""
    return SimpleNamespace(
        chat=SimpleNamespace(id=123),
        voice=SimpleNamespace(file_id="fake_id"),
        from_user=SimpleNamespace(id=42, username="tester"),
        text=None
    )
