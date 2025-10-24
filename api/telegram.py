import telebot
from telebot import types
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload
import json

# ======= توکن ربات =======
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"

# ======= خواندن Service Account JSON از فایل =======
# حتما قبلش این فایل رو تو Render در Secret Files آپلود کن
with open('service_account.json', 'r') as f:
    SERVICE_ACCOUNT_JSON = json.load(f)

# ======= اتصال به گوگل درایو =======
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_JSON)
drive_service = build('drive', 'v3', credentials=credentials)

# ======= ایجاد ربات =======
bot = telebot.TeleBot(TOKEN)

# ======= فانکشن دانلود فایل از گوگل درایو =======
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
    btn1 = types.InlineKeyboardButton("دریافت فایل 1", callback_data="file1")
    btn2 = types.InlineKeyboardButton("دریافت فایل 2", callback_data="file2")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "سلام! کدوم فایل میخوای دانلود کنی؟", reply_markup=markup)

# ======= هندلر دکمه ها =======
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "file1":
        file_id = "GOOGLE_DRIVE_FILE_ID_1"  # بجای این، آیدی فایل گوگل درایو بگذار
        fh = download_file(file_id)
        bot.send_audio(call.message.chat.id, fh, caption="فایل 1")
    elif call.data == "file2":
        file_id = "GOOGLE_DRIVE_FILE_ID_2"
        fh = download_file(file_id)
        bot.send_audio(call.message.chat.id, fh, caption="فایل 2")

# ======= اجرای ربات =======
bot.infinity_polling()
