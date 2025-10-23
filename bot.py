import os
import io
import json
from telebot import TeleBot, types
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from pydub import AudioSegment

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

# 🔹 گرفتن فایل‌های MP3
def get_mp3_files():
    results = drive_service.files().list(
        q="mimeType='audio/mpeg'",
        spaces='drive'
    ).execute()
    return results.get('files', [])

# 🔹 دانلود فایل در حافظه و تبدیل به MP3 در حافظه
def download_file_in_memory(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)

    # تبدیل با pydub به mp3
    audio = AudioSegment.from_file(fh)
    mp3_io = io.BytesIO()
    audio.export(mp3_io, format="mp3")
    mp3_io.seek(0)
    return mp3_io

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
    bot.answer_callback_query(call.id)  # پاسخ به callback تا دکمه timeout نشه
    file_id = call.data

    # دانلود و آماده‌سازی MP3 در حافظه
    mp3_file = download_file_in_memory(file_id)

    # ارسال فایل MP3 به کاربر
    bot.send_audio(call.message.chat.id, mp3_file, title="آهنگ شما")

# 🔹 اجرای ربات
bot.infinity_polling()
