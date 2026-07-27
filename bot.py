import os
import time
import pytz  # این خط برای حل مشکل اضافه شده است
from threading import Thread
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = "8671187176:AAFby5lrme-3dAlgnEGLq0C-p-Yn9sXZ-EU"
CHANNEL_ID = -1006474221

bot = Bot(token=BOT_TOKEN)

posts = [
    "🔒 Never share your Secret Recovery Phrase.",
    "⚠️ Beware of fake Trust Wallet websites.",
    "🔐 Always enable two-factor authentication.",
    "📥 Download Trust Wallet only from the official website."
]

index = 0

def send_post():
    global index
    if CHANNEL_ID and BOT_TOKEN:
        bot.send_message(
            chat_id=CHANNEL_ID,
            text=posts[index % len(posts)]
        )
        index += 1

# منطقه زمانی به وقت ایران (تهران) تنظیم شد
tz = pytz.timezone('Asia/Tehran')

# اضافه کردن منطقه زمانی به زمان‌بند
scheduler = BackgroundScheduler(timezone=tz)

# این زمان‌ها حالا دقیقاً بر اساس ساعت ایران محاسبه می‌شوند
scheduler.add_job(send_post, "cron", hour=9)   # ۹ صبح به وقت ایران
scheduler.add_job(send_post, "cron", hour=15)  # ۳ بعد از ظهر به وقت ایران
scheduler.add_job(send_post, "cron", hour=21)  # ۹ شب به وقت ایران
scheduler.start()

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    print("Bot is running...")
    
    # این حلقه برای این است که برنامه اصلی بسته نشود و زمان‌بند بتواند به کار خود ادامه دهد
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
