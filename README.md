<h1>🤖 Telegram Gemini Bot (Nalayak)</h1>

A production-ready Telegram AI Assistant Bot powered by Google Gemini API, deployed on Railway, and enhanced with:

- Text chat (short, friendly buddy-style replies)

- Voice input + voice reply (speech-to-text + text-to-speech)

- Image input with prompt (analyze images with Gemini)

- Database logging (stores all messages & replies for future use)

You can try this bot on telegram - [Try Bot](https://t.me/nalyakbot) 

<h2>Features</h2>

- Text Handler → Chat like a friend, short & casual replies.

- Voice Handler → Send a voice message, bot replies back in voice + text.

- Image Handler → Send an image (with optional caption prompt), bot analyzes it and replies.

- Database Integration → All conversations (text, voice, image) are logged into a PostgreSQL DB.

<h2>⚙️ Setup Instructions</h2>
1️. Clone this repository

``git clone https://github.com/yourusername/gemini-telegram-bot.git``

``cd gemini-telegram-bot``

2️. Install dependencies

``pip install -r requirements.txt``

3️. Configure Environment Variables

Create a .env file in the root folder:

``TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=postgresql+psycopg2://username:password@host:port/dbname``


👉 On Railway, you can add these as project variables.

4️. Run locally

``python -m app.bot``

5️. Run with Docker

Build and run the container:

``docker build -t gemini-bot .
docker run -d --name gemini-bot -e TELEGRAM_BOT_TOKEN=xxx -e GEMINI_API_KEY=xxx -e DATABASE_URL=xxx gemini-bot``

<h2>🚀 Deployment (Railway)</h2>

Push code to GitHub.

Create a new Railway project → Deploy from GitHub repo.

Add environment variables in Railway dashboard:

TELEGRAM_BOT_TOKEN

GEMINI_API_KEY

DATABASE_URL (Railway provides Postgres, copy the connection URL).

<h2>Deploy</h2>

<h2>🛠️ Tech Stack</h2>

Python 3.12

TeleBot (pyTelegramBotAPI)

Google Generative AI (Gemini)

SpeechRecognition + gTTS + pydub (for voice handling)

PostgreSQL + SQLAlchemy ORM (for persistence)

Docker (for containerized deployment)

Railway (for hosting)

<h2>📖 Usage</h2>

Send a text message → Bot replies casually.

Send a voice message → Bot replies back in voice + text.

Send an image with caption → Bot analyzes + responds.

All chats are stored in DB for logs/analytics.