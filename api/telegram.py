import telebot
from telebot import types
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# -------------------- تنظیمات --------------------
TOKEN = '5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI'
SERVICE_ACCOUNT_FILE = 'service_account.json'

# فایل‌های گوگل درایو
files = {
    "فایل 1": "1S_YDwN74axzBGm_g1rbMcQ_zk8ChAkR1",
    "فایل 2": "1vNLCT34rY2y8NkiSkRwCu3MBlxholRYG",
    "فایل 3": "1RvoEBbJXHd-rzVuR5TVd0u4wxkhJM6Tt",
    "فایل 4": "1MAAaoAfbNxhr8jeE6I4FDnhy4A9RA5gm",
    "فایل 5": "1yMT25ytHmpwNwc-Q6Lq48Cv5b5RLlmpc"
}

# -------------------- راه‌اندازی Google Drive API --------------------
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('drive', 'v3', credentials=credentials)

# -------------------- راه‌اندازی ربات --------------------
bot = telebot.TeleBot(TOKEN)

# -------------------- منو اصلی --------------------
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for name in files.keys():
        markup.add(types.KeyboardButton(name))
    return markup

# -------------------- دریافت فایل از گوگل درایو --------------------
def get_file_link(file_id):
    # ساخت لینک مستقیم دانلود گوگل درایو
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# -------------------- هندلر استارت --------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "کدوم فایل رو میخوای دانلود کنی؟",
        reply_markup=main_menu()
    )

# -------------------- هندلر انتخاب فایل --------------------
@bot.message_handler(func=lambda message: message.text in files)
def send_file(message):
    file_id = files[message.text]
    link = get_file_link(file_id)
    bot.send_message(
        message.chat.id,
        f"اینجا لینک دانلود فایل {message.text}:\n{link}"
    )

# -------------------- اجرای ربات --------------------
print("Bot is running...")
bot.infinity_polling()
