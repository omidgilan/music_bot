import telebot
from telebot import types
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# ====== تنظیمات ربات ======
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"
bot = telebot.TeleBot(TOKEN)

# ====== تنظیمات گوگل درایو ======
SERVICE_ACCOUNT_JSON = """
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "...",
  "token_uri": "...",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
"""  # اینو از Secret Files بخون، نه اینجا مستقیم

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
credentials = Credentials.from_service_account_info(
    eval(SERVICE_ACCOUNT_JSON.replace('\n',''))
)
drive_service = build('drive', 'v3', credentials=credentials)

# ====== دستور /start ======
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🎵 آهنگ 1", callback_data="music_1")
    btn2 = types.InlineKeyboardButton("🎵 آهنگ 2", callback_data="music_2")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "سلام! آهنگ موردنظر خود را انتخاب کن:", reply_markup=markup)

# ====== هندل دکمه‌ها ======
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "music_1":
        send_drive_file(call.message.chat.id, "GOOGLE_FILE_ID_1")
    elif call.data == "music_2":
        send_drive_file(call.message.chat.id, "GOOGLE_FILE_ID_2")

# ====== ارسال فایل از گوگل درایو ======
def send_drive_file(chat_id, file_id):
    request = drive_service.files().get_media(fileId=file_id)
    from io import BytesIO
    from telebot.types import InputFile
    fh = BytesIO()
    downloader = telebot.util.download_file(request, fh)
    fh.seek(0)
    bot.send_audio(chat_id, fh)

# ====== اجرای ربات ======
bot.infinity_polling()
