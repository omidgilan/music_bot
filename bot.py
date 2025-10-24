import telebot

# 🔹 توکن جدید ربات
TOKEN = "5564295105:AAFUmzvcsFWpYl7y0cnUc6tsHLkbVGNoQSU"
bot = telebot.TeleBot(TOKEN)

# 🔹 فرمان /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "ربات با موفقیت آنلاین شد! ✅")

# 🔹 اجرا
bot.polling(none_stop=True)
