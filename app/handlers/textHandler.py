from app.services.geminiService import ask_gemini
from telebot import TeleBot
from app.services.database import SessionLocal, MessageLog

def register_text_handler(bot: TeleBot):
    @bot.message_handler(func = lambda msg: msg.text and not msg.text.startswith('/'))
    def handle_text(message):
        user_input = message.text
        print(f"[USER] {message.from_user.username or message.chat.id}: {user_input}")

        try:
            answer = ask_gemini(user_input)
            bot.reply_to(message, answer)
        except Exception as e:
            bot.reply_to(message, f"Error: {str(e)}")

def save_message(user_id, input_type, content, reply):
    db = SessionLocal()
    msg = Message(user_id=user_id, input_type=input_type, content=content, reply=reply)
    db.add(msg)
    db.commit()
    db.close()

    reply = ask_gemini(text)
    save_message(message.from_user.id, "text", text, reply)
    save_message(str(message.from_user.id), "voice", text)
    save_message(str(message.from_user.id), "image", f"{prompt} | image sent")
    bot.reply_to(message, reply)