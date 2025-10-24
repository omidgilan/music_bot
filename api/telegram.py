import io
from telebot import TeleBot, types
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

# ======= توکن ربات =======
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"

# ======= اتصال به گوگل درایو =======
# مطمئن شو فایل service_account.json در ریشه پروژه هست
credentials = Credentials.from_service_account_file('service_account.json')
drive_service = build('drive', 'v3', credentials=credentials)

# ======= ایجاد ربات =======
bot = TeleBot(TOKEN)

# ======= فانکشن دانلود فایل =======
def download_file(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# ======= هندلر /start =======
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
        fh = download_file("GOOGLE_DRIVE_FILE_ID_1")  # آیدی فایل گوگل درایو خودت
        bot.send_audio(call.message.chat.id, fh, caption="فایل 1")
    elif call.data == "file2":
        fh = download_file("GOOGLE_DRIVE_FILE_ID_2")
        bot.send_audio(call.message.chat.id, fh, caption="فایل 2")

# ======= اجرای ربات =======
bot.infinity_polling()
