from telebot import TeleBot
from app.services.geminiService import ask_gemini
from app.services.database import SessionLocal, MessageLog


def save_message(user_id, message_type, content):
    """Save a message (user input or bot reply) to the database"""
    db = SessionLocal()
    try:
        msg = MessageLog(user_id=str(user_id), message_type=message_type, content=content)
        db.add(msg)
        db.commit()
    finally:
        db.close()


def register_text_handler(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text and not msg.text.startswith('/'))
    def handle_text(message):
        user_input = message.text
        print(f"[USER] {message.from_user.username or message.chat.id}: {user_input}")

        try:
            # Save user input
            save_message(message.from_user.id, "text", user_input)

            # Get reply from Gemini
            reply = ask_gemini(user_input)

            # Save bot reply
            save_message(message.from_user.id, "bot_reply", reply)

            # Send reply back to Telegram
            bot.reply_to(message, reply)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            bot.reply_to(message, error_msg)