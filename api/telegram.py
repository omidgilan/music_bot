import telebot

# ======= توکن ربات =======
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"

# ======= ایجاد ربات =======
bot = telebot.TeleBot(TOKEN)

# ======= هندلر دستور /start =======
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! ربات الان آنلاین شد ✅")

# ======= اجرای ربات =======
bot.infinity_polling()
