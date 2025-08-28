import re
from telebot import TeleBot
from app.services.shortenerService import shorten_url, get_user_links, delete_link

# simple URL regex for inline detection
URL_PATTERN = re.compile(r"(https?://[^\s]+)", re.IGNORECASE)

def register_url_handler(bot: TeleBot):

    @bot.message_handler(func=lambda m: bool(m.text) and URL_PATTERN.search(m.text))
    def handle_inline_urls(message):
        
        match = URL_PATTERN.search(message.text or "")
        if not match:
            return
        url = match.group(1)

        user_id = message.from_user.id
        short = shorten_url(user_id=user_id, original_url=url)
        if short:
            bot.reply_to(message, f"✅ Shortened: {short}")
        else:
            bot.reply_to(message, "⚠️ Could not shorten that URL. Please try again.")

    @bot.message_handler(commands=["my_links"])
    def my_links(message):
        user_id = message.from_user.id
        links = get_user_links(user_id)
        if not links:
            bot.reply_to(message, "You have no links yet. Send a URL and I’ll shorten it!")
            return

        lines = [
            f"{l.id}. {l.short_code} → {l.original_url}"
            for l in links[:20]   
        ]
        bot.reply_to(message, "🔗 Your links:\n" + "\n".join(lines))

    @bot.message_handler(commands=["delete"])
    def delete_cmd(message):
        parts = (message.text or "").strip().split()
        if len(parts) != 2 or not parts[1].isdigit():
            bot.reply_to(message, "Usage: /delete <link_id>")
            return
        link_id = int(parts[1])
        ok = delete_link(message.from_user.id, link_id)
        bot.reply_to(message, "🗑️ Deleted." if ok else "❌ Could not delete.")
