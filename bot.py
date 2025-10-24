import telebot
from telebot import types
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload

# ======= توکن ربات =======
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"

# ======= مسیر فایل Service Account JSON =======
SERVICE_ACCOUNT_FILE = 'service_account.json'

# ======= اتصال به گوگل درایو =======
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
drive_service = build('drive', 'v3', credentials=credentials)

# ======= ایجاد ربات =======
bot = telebot.TeleBot(TOKEN)

# ======= دانلود فایل از گوگل درایو =======
def download_file(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# ======= هندلر دستور /start =======
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    # دکمه های شیشه‌ای
    btn1 = types.InlineKeyboardButton("دریافت فایل 1", callback_data="file1")
    btn2 = types.InlineKeyboardButton("دریافت فایل 2", callback_data="file2")
    btn3 = types.InlineKeyboardButton("دریافت فایل 3", callback_data="file3")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "سلام! کدوم فایل میخوای دانلود کنی؟", reply_markup=markup)

# ======= هندلر دکمه ها =======
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # آیدی فایل‌های گوگل درایو
    files = {
        "file1": "GOOGLE_DRIVE_FILE_ID_1",
        "file2": "GOOGLE_DRIVE_FILE_ID_2",
        "file3": "GOOGLE_DRIVE_FILE_ID_3"
    }
    file_id = files.get(call.data)
    if file_id:
        fh = download_file(file_id)
        bot.send_audio(call.message.chat.id, fh, caption=f"فایل {call.data[-1]}")

# ======= اجرای ربات =======
bot.infinity_polling()
