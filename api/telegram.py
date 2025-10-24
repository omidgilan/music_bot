import telebot
from telebot import types
import requests
from io import BytesIO

# توکن رباتت
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"
bot = telebot.TeleBot(TOKEN)

# لیست فایل‌ها و لینک گوگل درایو
# کلید: نام فایل روی دکمه، مقدار: لینک دانلود مستقیم
FILES = {
    "فایل 1": "https://drive.google.com/uc?export=download&id=1YXTFSarpMT7fbsYEkfrKWAKGA3fTgyIw",
    "فایل 2": "https://drive.google.com/uc?export=download&id=1c2XfAg8moYF5bK9U8eCqg1TCeLZhhFq1",
    "فایل 3": "https://drive.google.com/uc?export=download&id=1PU8cF1KuZ-mHyw9ukFbbPSK8FRGigkgd"
}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    for name in FILES.keys():
        markup.add(types.InlineKeyboardButton(name, callback_data=name))
    bot.send_message(message.chat.id, "کدوم فایل رو میخوای دانلود کنی؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    file_name = call.data
    file_url = FILES[file_name]

    bot.send_message(call.message.chat.id, f"در حال ارسال {file_name} ...")
    try:
        r = requests.get(file_url)
        r.raise_for_status()
        bot.send_audio(call.message.chat.id, BytesIO(r.content), title=file_name)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"خطا در ارسال فایل: {str(e)}")

bot.polling(none_stop=True)
