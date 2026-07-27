from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from config import BOT_TOKEN, CHANNEL_ID

bot = Bot(token=BOT_TOKEN)

posts = [
    "🔐 Never share your Secret Recovery Phrase with anyone.",
    "⚠️ Beware of fake Trust Wallet websites and phishing links.",
    "🛡️ Always enable two-factor authentication where available.",
    "📚 Download Trust Wallet only from the official website or app stores."
]

index = 0

def send_post():
    global index
    bot.send_message(chat_id=CHANNEL_ID, text=posts[index % len(posts)])
    index += 1

scheduler = BlockingScheduler()

scheduler.add_job(send_post, "cron", hour=9, minute=0)
scheduler.add_job(send_post, "cron", hour=15, minute=0)
scheduler.add_job(send_post, "cron", hour=21, minute=0)

print("Bot is running...")
scheduler.start()
