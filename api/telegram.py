import os
import json
import telebot
from telebot import types
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# ======= تنظیمات ربات =======
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"
bot = telebot.TeleBot(TOKEN)

# ======= خواندن فایل JSON سرویس اکانت گوگل =======
SERVICE_ACCOUNT_JSON = os.environ.get("SERVICE_ACCOUNT_JSON")
if not SERVICE_ACCOUNT_JSON:
    raise Exception("SERVICE_ACCOUNT_JSON not found in environment variables!")

service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

# ======= اتصال به گوگل درایو =======
drive_service = build('drive', 'v3', credentials=credentials)

# ======= توابع کمکی =======
def get_file_from_drive(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

def create_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("❤️ پسند", callback_data="like"),
        types.InlineKeyboardButton("🔁 اشتراک", switch_inline_query=""),
        types.InlineKeyboardButton("⬆️ بالا", callback_data="up")
    )
    return keyboard

# ======= هندلر استارت =======
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "سلام! ربات آماده است.")

# ======= هندلر دریافت فایل =======
@bot.message_handler(commands=['mp3'])
def send_mp3(message):
    # اینجا باید ID فایل گوگل درایو رو بذاری
    file_id = "YOUR_DRIVE_FILE_ID_HERE"
    try:
        file_data = get_file_from_drive(file_id)
        bot.send_audio(message.chat.id, file_data, reply_markup=create_inline_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا در ارسال فایل: {e}")

# ======= هندلر دکمه‌ها =======
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "like":
        bot.answer_callback_query(call.id, "پسندیدید! ❤️")
    elif call.data == "up":
        bot.answer_callback_query(call.id, "به بالا رفتید ⬆️")

# ======= اجرای ربات =======
bot.infinity_polling()
