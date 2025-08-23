from services.geminiService import ask_gemini
from telebot import TeleBot

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