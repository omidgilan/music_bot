import telebot
from telebot import types
import requests
import os

# 🔹 توکن رباتت
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"
bot = telebot.TeleBot(TOKEN)

# 🔹 فایل‌های گوگل درایو (برای تست فقط دو تا فایل)
FILES = {
    "فایل ۲": "https://drive.google.com/uc?export=download&id=1c2XfAg8moYF5bK9U8eCqg1TCeLZhhFq1",
    "فایل ۳": "https://drive.google.com/uc?export=download&id=1PU8cF1KuZ-mHyw9ukFbbPSK8FRGigkgd"
}

# صفحه اصلی با دکمه‌ها
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for name in FILES.keys():
        markup.add(types.InlineKeyboardButton(name, callback_data=name))
    bot.send_message(message.chat.id, "کدوم فایل رو میخوای دانلود کنی؟", reply_markup=markup)

# پاسخ به کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    file_url = FILES.get(call.data)
    if file_url:
        bot.answer_callback_query(call.id, f"در حال ارسال {call.data} ...")
        # دانلود فایل موقت
        r = requests.get(file_url, stream=True)
        filename = f"{call.data}.mp3"
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        # ارسال فایل
        with open(filename, "rb") as f:
            bot.send_audio(call.message.chat.id, f)
        os.remove(filename)

bot.polling()
