import telebot
from telebot import types
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload

# توکن ربات تلگرام
TOKEN = 'توکن_ربات_تو_اینجا'

# مسیر فایل Service Account JSON
SERVICE_ACCOUNT_FILE = 'service_account.json'

# اتصال به گوگل درایو
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
drive_service = build('drive', 'v3', credentials=credentials)

# ایجاد ربات تلگرام
bot = telebot.TeleBot(TOKEN)

# دیکشنری آیدی فایل‌ها
files = {
    "file1": "1S_YDwN74axzBGm_g1rbMcQ_zk8ChAkR1",
    "file2": "1vNLCT34rY2y8NkiSkRwCu3MBlxholRYG",
    "file3": "1RvoEBbJXHd-rzVuR5TVd0u4wxkhJM6Tt",
    "file4": "1MAAaoAfbNxhr8jeE6I4FDnhy4A9RA5gm",
    "file5": "1yMT25ytHmpwNwc-Q6Lq48Cv5b5RLlmpc"
}

# دانلود فایل از گوگل درایو
def download_file(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# هندلر دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    # دکمه‌های شیشه‌ای
    btn1 = types.InlineKeyboardButton("دریافت فایل 1", callback_data="file1")
    btn2 = types.InlineKeyboardButton("دریافت فایل 2", callback_data="file2")
    btn3 = types.InlineKeyboardButton("دریافت فایل 3", callback_data="file3")
    btn4 = types.InlineKeyboardButton("دریافت فایل 4", callback_data="file4")
    btn5 = types.InlineKeyboardButton("دریافت فایل 5", callback_data="file5")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "سلام! کدوم فایل میخوای دانلود کنی؟", reply_markup=markup)

# هندلر دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    file_id = files.get(call.data)
    if file_id:
        fh = download_file(file_id)
        bot.send_audio(call.message.chat.id, fh, caption=f"فایل {call.data[-1]}")

# اجرای ربات
bot.infinity_polling()
