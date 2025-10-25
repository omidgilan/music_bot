import telebot

# توکن ربات رو اینجا بذار
TOKEN = "5548149661:AAFblu4NL86utR9SbzuE6RQ27HuD3Uiynas"
bot = telebot.TeleBot(TOKEN)

# وقتی کاربر /start رو ارسال کرد
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! ربات تستی فعال شد ✅")

# فعال کردن ربات (Polling)
print("Bot is polling...")  # فقط برای اطلاع توی ترمینال
bot.polling()
