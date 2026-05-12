from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": user_text}
            ]
        }
    )

    reply = r.json()["choices"][0]["message"]["content"]

    await update.message.reply_text(reply[:4000])

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle))

print("Bot running...")
app.run_polling()
