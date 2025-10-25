import telebot
from telebot import types
import requests

# توکن ربات
TOKEN = "5548149661:AAFblu4NL86utR9SbzuE6RQ27HuD3Uiynas"
bot = telebot.TeleBot(TOKEN)

# لیست آهنگ‌ها (اسم آهنگ: لینک دانلود مستقیم)
songs = {
    "ترانه ۱ - هنرمند ناشناس": "https://drive.google.com/uc?id=1c2XfAg8moYF5bK9U8eLZhhFq1&export=download",
    "ترانه ۲ - هنرمند ناشناس": "https://drive.google.com/uc?id=1PU8cF1KuZ-mHyw9ukFbbPSK8FRGigkgd&export=download"
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    for song_name in songs.keys():
        button = types.InlineKeyboardButton(song_name, callback_data=song_name)
        markup.add(button)
    bot.send_message(message.chat.id, "کدوم آهنگ رو میخوای دانلود کنی؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    file_name = call.data
    file_url = songs[file_name]
    bot.answer_callback_query(call.id, text=f"در حال ارسال {file_name} ...")
    
    # دانلود فایل از گوگل درایو
    response = requests.get(file_url)
    
    if response.status_code == 200:
        bot.send_audio(call.message.chat.id, response.content, title=file_name)
    else:
        bot.send_message(call.message.chat.id, "خطا در دانلود فایل!")

bot.polling(none_stop=True)
