import telebot
from telebot import types
import requests

# 🔹 توکن جدید ربات
TOKEN = "5564295105:AAFUmzvcsFWpYl7y0cnUc6tsHLkbVGNoQSU"
bot = telebot.TeleBot(TOKEN)

# 🔹 لیست فایل‌ها با لینک مستقیم گوگل درایو (نمونه دو فایل)
files = {
    "فایل 1": "https://drive.google.com/uc?export=download&id=1c2XfAg8moYF5bK9U8eCqg1TCeLZhhFq1",
    "فایل 2": "https://drive.google.com/uc?export=download&id=1PU8cF1KuZ-mHyw9ukFbbPSK8FRGigkgd"
}

# 🔹 فرمان /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for f in files.keys():
        markup.add(types.KeyboardButton(f))
    bot.send_message(message.chat.id, "کدوم فایل رو میخوای دانلود کنی؟", reply_markup=markup)

# 🔹 دریافت پیام و ارسال فایل
@bot.message_handler(func=lambda message: True)
def send_file(message):
    file_name = message.text
    if file_name in files:
        url = files[file_name]
        bot.send_message(message.chat.id, f"در حال ارسال {file_name} ...")
        bot.send_document(message.chat.id, document=url)
    else:
        bot.send_message(message.chat.id, "فایل پیدا نشد، لطفاً یکی از دکمه‌ها را انتخاب کن.")

# 🔹 اجرا
bot.polling(none_stop=True)
