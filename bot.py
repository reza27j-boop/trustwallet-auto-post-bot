import os
import asyncio
import pytz
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = "8671187176:AAFby5lrme-3dAlg..."
CHANNEL_ID = -1006474221

bot = Bot(token=BOT_TOKEN)

posts = [
    "Never share your Secret Recovery Phrase with anyone!",
    "Beware of fake Trust Wallet websites!",
    "Always enable two-factor authentication!",
    "Download Trust Wallet only from the official store!"
]

index = 0

# تابع ارسال پیام به صورت async برای سازگاری با نسخه جدید python-telegram-bot
async def send_post_async():
    global index
    if CHANNEL_ID and BOT_TOKEN:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=posts[index % len(posts)]
        )
        index += 1

# اجرا کننده تابع async در سیستم زمان‌بندی
def send_post():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(send_post_async())

# تنظیمات زمان‌بندی
tz = pytz.timezone('Asia/Tehran')
scheduler = BackgroundScheduler(timezone=tz)

scheduler.add_job(send_post, "cron", hour=9)
scheduler.add_job(send_post, "cron", hour=15)
scheduler.add_job(send_post, "cron", hour=21)
scheduler.start()

# تنظیمات سرور وب برای Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
scheduler.start()

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    run_web()
