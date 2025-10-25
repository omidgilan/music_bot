import telebot

# توکن جدید رباتت
TOKEN = "5548149661:AAFblu4NL86utR9SbzuE6RQ27HuD3Uiynas"
bot = telebot.TeleBot(TOKEN)

# فرمان /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! ربات تستی آنلاین شد ✅")

# پاسخ ساده به پیام متنی
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "ربات آنلاین است و پیام شما را دریافت کرد!")

# شروع ربات
print("ربات در حال اجراست...")
bot.infinity_polling()
