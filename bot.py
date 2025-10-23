import os
import io
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# -----------------------------
# تنظیمات امن با Secret
# -----------------------------
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # توکن ربات از Vercel Secret
SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GOOGLE_DRIVE_JSON"))  # JSON Service Account از Secret
FOLDER_ID = "YOUR_FOLDER_ID"  # آیدی پوشه گوگل درایو

bot = telebot.TeleBot(TOKEN)

# -----------------------------
# اتصال به گوگل درایو
# -----------------------------
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO,
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)
drive_service = build('drive', 'v3', credentials=credentials)

# -----------------------------
# دریافت لیست فایل‌ها
# -----------------------------
def list_files():
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='audio/mpeg'",
        pageSize=50,
        fields="files(id, name)"
    ).execute()
    return results.get('files', [])

# -----------------------------
# دانلود فایل
# -----------------------------
def download_file(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# -----------------------------
# دکمه شیشه‌ای اصلی
# -----------------------------
def music_inline_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("↑ لیست آهنگ‌ها", callback_data="show_list"))
    return markup

# -----------------------------
# دستور /start
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "سلام! لیست آهنگ‌ها رو با دکمه زیر ببینید:", reply_markup=music_inline_keyboard())

# -----------------------------
# هندلر دکمه‌های Inline
# -----------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "show_list":
        files = list_files()
        markup = InlineKeyboardMarkup()
        for f in files:
            # هر آهنگ یه دکمه جدا داره با callback_data = id فایل
            markup.add(InlineKeyboardButton(f"🎵 {f['name']}", callback_data=f['id']))
        bot.send_message(call.message.chat.id, "لیست آهنگ‌ها:", reply_markup=markup)
    
    else:
        # callback_data = id فایل
        file_id = call.data
        bot.answer_callback_query(call.id, "در حال ارسال آهنگ...")
        audio_file = download_file(file_id)
        bot.send_audio(call.message.chat.id, audio_file)

# -----------------------------
# اجرای ربات
# -----------------------------
bot.polling()
