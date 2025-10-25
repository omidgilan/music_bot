# bot.py
import telebot
from api import telegram  # import از فولدر api
import os

# 🔹 توکن ربات جدیدت رو اینجا قرار بده
TOKEN = "5548149661:AAFblu4NL86utR9SbzuE6RQ27HuD3Uiynas"

bot = telebot.TeleBot(TOKEN)

# پیام اولیه
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! ربات آنلاین است ✅")

# پیام تستی ساده
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "پیام دریافت شد: " + message.text)

# اجرا
if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.polling(none_stop=True)
