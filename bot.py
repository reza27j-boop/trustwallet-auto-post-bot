import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from duckduckgo_search import DDGS

# توکن ربات
TOKEN = "8911274145:AAGiq-SOURGaw38vb2kgUU_iAuRf9DgiKcU"

# آیدی کانال شما
CHANNEL_ID = "@akhbararzdigtali" 

# شناسه چت ادمین
ADMIN_CHAT_ID = None  

# متن ثابت پشتیبانی جهت اضافه شدن به انتهای پست‌ها
SUPPORT_FOOTER = (
    "\n\nبرای دریافت اموزش و رفع مشکل و راهنمایی با پشتیبانی ۲۴ ساعته در ارتباط باشید\n"
    "ID support :https://t.me/TrustWalletsuportadmin"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔴 خطای تراکنش معلق (Pending)", callback_data="err_pending")],
        [InlineKeyboardButton("🟡 خطای عدم بروزرسانی موجودی", callback_data="err_balance")],
        [InlineKeyboardButton("🔵 خطای عدم کفایت کارمزد (Gas Fee)", callback_data="err_gas")],
        [InlineKeyboardButton("🟢 خطای عدم اتصال به شبکه", callback_data="err_network")],
        [InlineKeyboardButton("🟣 راهنمای شناسایی توکن سفارشی", callback_data="err_token")],
        [InlineKeyboardButton("💬 ارتباط با بخش راهنما", callback_data="contact")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "👋 به سیستم راهنما و عیب‌یابی خطاهای شبکه خوش آمدید.\n\n"
        "لطفاً موضوع مورد نظر را جهت ارسال به کانال انتخاب کنید:"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu_keyboard())
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "main_menu":
        await start(update, context)
        return

    # انتخاب متن راهنما بر اساس دکمه فشرده شده
    if query.data == "err_pending":
        text = (
            "📌 **تراکنش معلق (Pending):**\n\n"
            "این حالت زمانی رخ می‌دهد که شبکه شلوغ است.\n"
            "• میزان کارمزد تعیین‌شده را بررسی کنید.\n"
            "• تا زمان تأیید نهایی توسط بلاک‌چین صبوری کنید."
        )
        search_query = "crypto pending transaction error"
    elif query.data == "err_balance":
        text = (
            "📌 **عدم نمایش موجودی:**\n\n"
            "• وضعیت اتصال اینترنت و تغییر IP را بررسی کنید.\n"
            "• برنامه را یک‌بار به طور کامل ببندید و دوباره باز کنید."
        )
        search_query = "crypto wallet balance error"
    elif query.data == "err_gas":
        text = (
            "📌 **خطای کارمزد (Gas Fee):**\n\n"
            "برای انجام هر تراکنش در شبکه، داشتن مقدار کمی از ارز اصلی همان شبکه (مانند BNB یا ETH) برای پرداخت هزینه پردازش الزامی است."
        )
        search_query = "crypto gas fee error"
    elif query.data == "err_network":
        text = (
            "📌 **خطای اتصال:**\n\n"
            "سرور یا کشور ابزار تغییر IP خود را عوض کرده و پس از چند دقیقه مجدداً تلاش کنید."
        )
        search_query = "network connection error crypto"
    elif query.data == "err_token":
        text = (
            "📌 **شناسایی توکن:**\n\n"
            "از صحت آدرس قرارداد (Contract Address) و شبکه انتخاب‌شده اطمینان حاصل کنید."
        )
        search_query = "custom token contract address"
    elif query.data == "contact":
        text = (
            "💬 **ارسال پیام به پشتیبانی:**\n\n"
            "لطفاً سوال یا پیام خود را همین‌جا ارسال کنید. کارشناسان ما به زودی پاسخ شما را خواهند داد."
        )
        search_query = ""
    else:
        text = "راهنمایی یافت نشد."
        search_query = ""

    # جستجوی عکس مرتبط
    image_url = None
    if search_query:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(search_query, max_results=1))
                if results:
                    image_url = results[0].get("image")
        except Exception as e:
            logging.error(f"Image search error: {e}")

    # افزودن پاورقی پشتیبانی به انتهای متن پست
    final_text = text + SUPPORT_FOOTER

    # ارسال پست به کانال
    try:
        if image_url:
            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=image_url,
                caption=final_text,
                parse_mode="Markdown"
            )
        else:
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=final_text,
                parse_mode="Markdown"
            )
        await query.answer("✅ پست با موفقیت به کانال ارسال شد.", show_alert=True)
    except Exception as e:
        logging.error(f"Error sending to channel: {e}")
        await query.answer("❌ خطا در ارسال پست به کانال. بررسی کنید ربات ادمین کانال باشد.", show_alert=True)

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ADMIN_CHAT_ID
    user = update.effective_user
    chat_id = update.effective_chat.id

    if ADMIN_CHAT_ID and chat_id == ADMIN_CHAT_ID:
        if update.message.reply_to_message:
            try:
                original_msg = update.message.reply_to_message.text or update.message.reply_to_message.caption
                target_user_id = int(original_msg.split("🆔 ID: ")[1].split("\n")[0])
                
                if update.message.text:
                    await context.bot.send_message(
                        chat_id=target_user_id,
                        text=f"👨‍💻 **پاسخ پشتیبانی:**\n\n{update.message.text}",
                        parse_mode="Markdown"
                    )
                elif update.message.photo:
                    await context.bot.send_photo(
                        chat_id=target_user_id,
                        photo=update.message.photo[-1].file_id,
                        caption=f"👨‍💻 **پاسخ پشتیبانی:**\n\n{update.message.caption or ''}",
                        parse_mode="Markdown"
                    )
                await update.message.reply_text("✅ پاسخ شما با موفقیت برای کاربر ارسال شد.")
            except Exception:
                await update.message.reply_text("❌ خطا در ارسال. حتماً روی پیام ارسال‌شده از طرف ربات (که حاوی 🆔 ID است) Reply کنید.")
        return

    if user.username == "Mohamdbg" or ADMIN_CHAT_ID is None:
        ADMIN_CHAT_ID = chat_id
        print(f"شناسه چت ادمین ست شد: {ADMIN_CHAT_ID}")

    user_info = (
        f"📩 **پیام جدید از کاربر:**\n"
        f"👤 نام: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"🔗 آیدی: @{user.username if user.username else 'ندارد'}\n\n"
        f"💬 **متن پیام:**\n"
    )
    
    if update.message.text:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=user_info + update.message.text,
            parse_mode="Markdown"
        )
    elif update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=user_info + (update.message.caption or ""),
            parse_mode="Markdown"
        )

    await update.message.reply_text("✅ پیام شما دریافت شد و به پشتیبانی ارسال گردید. به زودی پاسخ خود را دریافت خواهید کرد.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_messages))

    print("ربات با موفقیت فعال شد و در حال اجرا است...")
    app.run_polling()

if __name__ == "__main__":
    main()
