import telebot

# توکن ربات
TOKEN = "5548149661:AAFblu4NL86utR9SbzuE6RQ27HuD3Uiynas"
bot = telebot.TeleBot(TOKEN)

# دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! ربات آنلاین است و آماده کار کردن.")

# پاسخ ساده به پیام‌ها
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "پیام دریافت شد: " + message.text)

# اجرای ربات
bot.polling()
