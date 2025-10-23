import os
import json
from telebot import TeleBot, types
from googleapiclient.discovery import build
from google.oauth2 import service_account
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

# 🔹 تابع گرفتن فایل‌های MP3 از گوگل درایو
def get_mp3_files():
    results = drive_service.files().list(
        q="mimeType='audio/mpeg'",
        spaces='drive'
    ).execute()
    return results.get('files', [])

# 🔹 تبدیل فایل به MP3 (اگر لازم بود)
def convert_to_mp3(input_path):
    output_path = os.path.splitext(input_path)[0] + ".mp3"
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="mp3")
    return output_path

# 🔹 دانلود فایل از گوگل درایو و تبدیل به MP3
def download_file(file_id, file_name):
    request = drive_service.files().get_media(fileId=file_id)
    local_path = f"/tmp/{file_name}"
    with open(local_path, "wb") as f:
        f.write(request.execute())
    return convert_to_mp3(local_path)

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
    bot.answer_callback_query(call.id)  # پاسخ به callback تا timeout نشه
    file_id = call.data
    file_info = drive_service.files().get(fileId=file_id, fields="name").execute()
    file_name = file_info['name']

    # 🔹 دانلود و تبدیل فایل
    mp3_path = download_file(file_id, file_name)

    # 🔹 ارسال فایل MP3
    with open(mp3_path, "rb") as audio:
        bot.send_audio(call.message.chat.id, audio, title=file_name)

# 🔹 اجرای ربات
bot.infinity_polling()
