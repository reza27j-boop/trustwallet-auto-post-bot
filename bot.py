import os
from threading import Thread
from flask import Flask

from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

posts = [
    "🔐 Never share your Secret Recovery Phrase.",
    "⚠️ Beware of fake Trust Wallet websites.",
    "🛡️ Always enable two-factor authentication.",
    "📚 Download Trust Wallet only from the official website."
]

index = 0

def send_post():
    global index
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=posts[index % len(posts)]
    )
    index += 1

scheduler = BlockingScheduler()

scheduler.add_job(send_post, "cron", hour=9)
scheduler.add_job(send_post, "cron", hour=15)
scheduler.add_job(send_post, "cron", hour=21)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

print("Bot is running...")
scheduler.start()
