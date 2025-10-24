import json
import os
import telebot
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from telebot import types

# توکن ربات
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"
bot = telebot.TeleBot(TOKEN)

# گرفتن JSON از Environment Variable
SERVICE_ACCOUNT_JSON = os.environ.get("SERVICE_ACCOUNT_JSON")
credentials = Credentials.from_service_account_info(json.loads(SERVICE_ACCOUNT_JSON))

# ساخت سرویس Google Drive
service = build('drive', 'v3', credentials=credentials)

# فرمان /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("دانلود MP3", callback_data="download")
    markup.add(button)
    bot.send_message(message.chat.id, "سلام! روی دکمه زیر بزن:", reply_markup=markup)

# پاسخ به دکمه
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "download":
        # ID فایل گوگل درایو
        file_id = 'YOUR_FILE_ID_HERE'
        request = service.files().get_media(fileId=file_id)
        with open("file.mp3", "wb") as f:
            downloader = request.execute()
            f.write(downloader)
        bot.send_audio(call.message.chat.id, open("file.mp3", "rb"))

# اجرا
bot.infinity_polling()
