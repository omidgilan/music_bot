import os
import json
from telebot import TeleBot, types
from googleapiclient.discovery import build
from google.oauth2 import service_account

# 🔹 توکن ربات
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = TeleBot(TOKEN)

# 🔹 دسترسی به گوگل درایو
SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_DRIVE_JSON")
credentials = service_account.Credentials.from_service_account_info(
    json.loads(SERVICE_ACCOUNT_JSON),
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)
drive_service = build('drive', 'v3', credentials=credentials)

# 🔹 تابع گرفتن فایل‌های MP3
def get_mp3_files():
    results = drive_service.files().list(
        q="mimeType='audio/mpeg'",
        spaces='drive'
    ).execute()
    return results.get('files', [])

# 🔹 دستور /start
@bot.message_handler(commands=['start'])
def start_message(message):
    files = get_mp3_files()
    if not files:
        bot.send_message(message.chat.id, "هیچ فایل موزیکی پیدا نشد! لطفاً فایل اضافه کنید.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for f in files:
        btn = types.InlineKeyboardButton(f['name'], callback_data=f['id'])
        markup.add(btn)

    bot.send_message(message.chat.id, "لیست آهنگ‌ها:", reply_markup=markup)

# 🔹 پاسخ به دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    file_id = call.data
    file = drive_service.files().get(fileId=file_id, fields="name, webContentLink").execute()
    bot.send_message(call.message.chat.id, f"دانلود فایل: {file['name']}\n{file['webContentLink']}")

# 🔹 اجرای ربات
bot.infinity_polling()
