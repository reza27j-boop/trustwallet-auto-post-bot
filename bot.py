import os
import asyncio
import pytz
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8671187176:AAFby5lrme-3dAlg...")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", -1006474221))

bot = Bot(token=BOT_TOKEN)

posts = [
    "Never share your Secret Recovery Phrase with anyone!",
    "Beware of fake Trust Wallet websites!",
    "Always enable two-factor authentication!",
    "Download Trust Wallet only from the official store!"
]

# متن پشتیبانی ثابت برای انتهای هر پست
SUPPORT_FOOTER = """

برای دریافت اموزش و رفع مشکل و راهنمایی با پشتیبانی ۲۴ ساعته در ارتباط باشید

ID support : https://t.me/your_support_handle"""

index = 0

async def send_post_async():
    global index
    if CHANNEL_ID and BOT_TOKEN:
        # ترکیب متن اصلی پست با متن پشتیبانی
        full_message = posts[index % len(posts)] + SUPPORT_FOOTER
        
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=full_message
        )
        index += 1

def send_post():
    """مدیریت ساخت و بستن حلقه async برای جلوگیری از خطای Runtime"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_post_async())
    finally:
        loop.close()

# تنظیمات زمان‌بندی (Scheduler)
tz = pytz.timezone('Asia/Tehran')
scheduler = BackgroundScheduler(timezone=tz)

scheduler.add_job(send_post, "cron", hour=9)
scheduler.add_job(send_post, "cron", hour=15)
scheduler.add_job(send_post, "cron", hour=21)
scheduler.start()

# تنظیمات وب‌سرور Flask برای هاستینگ
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
