import telebot
from telebot import types
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload

# ======= تنظیمات ربات =======
TELEGRAM_BOT_TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"

# ======= JSON سرویس اکانت گوگل =======
GOOGLE_SERVICE_ACCOUNT_JSON = {
    "type": "service_account",
    "project_id": "intricate-aria-458102-u2",
    "private_key_id": "068c000a1cafef96c783e9284f30cd7641f68a08",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC8rTDgTFUSdQjN
Aj3Tb+4732ElBC90d5A+0guVomu0Rm3gHx5Thhh1ywGCTM/4QpPqWfizCC/iyYw7
EQOy4KgpncDELq5Kohd4rV2ghQSnvptSBqVMYQF+VfqKNCaUFVEYICyqyiozM938
kUlruFMiFVCu2kogFpXjV7poCIG+ww6UTCjt4FBQgAv/3PM3MN3yNochH9btg7hK
sHXyzj0GnWg2/nU+UZbTsH736ezXju1Ry//mmBBo5V4CkfwOz1vhdQQnv4+DNV0K
/ZH/4G4u+lylmePSueb2LEiVpR75DkTJ0FgKZ8KBVHyhk8JezhFT4zD+hzcFga9c
MpcsGG1jAgMBAAECggEABHPS5S80MXGEWsxFa4dOdz8QCbk0WwMLav6vLOOJ1aiT
O70uX3fruVHGWowV6DFzqqvIz1iH6IYy5h3RhmEl0/ClDhwhbgrrBDs64NXFlX+v
NYbUcfRcbzhoujFuNwsKFvWDLfrWlThVNdSzS0s0SWBaoQrgHCtUvvG3bOkBilh5
7P6IfMgAsOlAVOQ/AG4QzSx05PI8VVEk2a7vGqsTvewgkzE/Obwophkw2fXvvmIC
yWR4x10tHk/PRxw7jFZmXbEqcDvU0QVRoDPK6n/1SRCCIS+F6798FVEzc8Q+n8gx
MrPLrz5+cLCsLz2ONmCff9ktjHd49QgRHfLiIMS78QKBgQDvGjotFAo5ZRAiKJx5
D7WxnEayc3kg/OD61uZlLIVacTa/L7CG7kNoTgflperUr8hMYDx/byZd3bosJ3Ec
811tBiS2gnDden6hmcJP0apvsKhO7j4X9f8BjiyPEwZGKExvyHPoZrwChNYnNHHz
5dvwMZpR24AZk6o4l1f2nBSWEQKBgQDKAqwg0aOuTN7A0dDEjLwTYk3NCUixWZqs
qkT2ReRZ2OArJ37CyVgG3BdWE2/1/S2h7uxAmsIFUJuX7C5XOwVds7LH9D1NPyLB
IUyojPQCDa2hw6VNfVt3rckZcIVb5m2SS5KT7qe1MkvH0PMy0X30Fyo1GahFF9G5
R5yptG4IMwKBgQCaRzMIiSi7tfE+CTRFjRRwwOSBGq8q0OCeGfHZkGuPWwO3Qx9F
QRHviIHh9Tfb+nxkg6glleOMp5gMC3sZ8hHzWgZwWSRYVETHIv5VIHU30iYXn/Qi
49CiAUnRG7ZtqG0Bp7baWwevHGVOMLHibQuIJYlsjhRO7I/mKglRD47c8QKBgQCx
y5JVvE10rkFrsf8tzrQF14KkUGSDe1rQV3gkzTUDAweh07wUkoOAXhvH7YmgFrog
CRo0bkEPzndzSjMrIU5Cv1M9+7AsmcHr+3Pt8UkduY41ju2hexCTEAir9EXbsb6E
gTE8NFO0/dSGxFgYRRu3RuAmJjPcw+8ZRHcVQjGJ0wKBgE+z9lMtA+cLcs5zQKzx
oPdGsLbPelZll0mejQUQfYqwGij9jhjg2mqP7oiy+Rjta5mnIvsYc54jDbovr0qZ
rp1owaEKDiNtqUL5DviSQcKWU+i2uovhGrcz9oI4fJlG27+F+1SmZSirXdR56YoT
emaJ2zeO7Dp7h/8zvSccYPs7
-----END PRIVATE KEY-----""",
    "client_email": "music-bot-sa@intricate-aria-458102-u2.iam.gserviceaccount.com",
    "client_id": "116282374376134538734",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/music-bot-sa@intricate-aria-458102-u2.iam.gserviceaccount.com"
}

# ======= اتصال به گوگل درایو =======
credentials = Credentials.from_service_account_info(GOOGLE_SERVICE_ACCOUNT_JSON)
drive_service = build('drive', 'v3', credentials=credentials)

# ======= ایجاد ربات =======
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

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

# ======= دستور /start =======
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("دانلود فایل 1", callback_data="file1")
    btn2 = types.InlineKeyboardButton("دانلود فایل 2", callback_data="file2")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "سلام! کدوم فایل رو میخوای دانلود کنی؟", reply_markup=markup)

# ======= هندلر دکمه‌ها =======
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "file1":
        file_id = "GOOGLE_DRIVE_FILE_ID_1"  # جایگزین با ID فایل واقعی
        fh = download_file(file_id)
        bot.send_audio(call.message.chat.id, fh, caption="فایل 1")
    elif call.data == "file2":
        file_id = "GOOGLE_DRIVE_FILE_ID_2"  # جایگزین با ID فایل واقعی
        fh = download_file(file_id)
        bot.send_audio(call.message.chat.id, fh, caption="فایل 2")

# ======= اجرای ربات =======
bot.infinity_polling()
