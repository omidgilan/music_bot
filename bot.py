import telebot
import json

# ====== تنظیمات ربات ======
TELEGRAM_TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ====== JSON حساب سرویس گوگل ======
SERVICE_ACCOUNT_JSON = """
{
  "type": "service_account",
  "project_id": "YOUR_PROJECT_ID",
  "private_key_id": "YOUR_PRIVATE_KEY_ID",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nYOUR_KEY\\n-----END PRIVATE KEY-----\\n",
  "client_email": "YOUR_CLIENT_EMAIL",
  "client_id": "YOUR_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "YOUR_CLIENT_X509_CERT_URL"
}
"""

service_account_info = json.loads(SERVICE_ACCOUNT_JSON)

# ====== نمونه دستور ساده ======
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! ربات آماده است 🎵")

# ====== اجرای ربات ======
if __name__ == "__main__":
    print("ربات داره اجرا میشه...")
    bot.polling(none_stop=True)
