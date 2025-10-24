import telebot
from telebot import types
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload

# ======= تنظیمات ربات =======
TOKEN = "توکن_ربات_تو"

# ======= Service Account JSON =======
SERVICE_ACCOUNT_JSON = {
    # JSON سرویس اکانتت رو اینجا بذار
}

# ======= اتصال به گوگل درایو =======
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_JSON)
drive_service = build('drive', 'v3', credentials=credentials)

# =====
