import telebot

# 🔹 توکن جدید رباتت
TOKEN = "5564295105:AAFUmzvcsFWpYl7y0cnUc6tsHLkbVGNoQSU"

bot = telebot.TeleBot(TOKEN)

# پاسخ به دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! ربات آماده است و آنلاین شد ✅")

# پاسخ به هر پیام متنی
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"پیام شما دریافت شد: {message.text}")

# اجرای ربات
bot.infinity_polling()
