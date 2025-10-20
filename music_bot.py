import telebot
from telebot import types
import json
import os

# 🟢 جای توکن خودت رو اینجا بگذار داخل کوتیشن‌ها:
TOKEN = "5564295105:AAExehUW8xw3SMc_vriJ6NWLLbn6qKSOSvI"

bot = telebot.TeleBot(TOKEN)
SONGS_FILE = "songs.json"

# --- ایجاد فایل در صورت نبود ---
if not os.path.exists(SONGS_FILE):
    with open(SONGS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# --- خواندن فایل آهنگ‌ها ---
def load_songs():
    with open(SONGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --- ذخیره فایل آهنگ‌ها ---
def save_songs(songs):
    with open(SONGS_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)

# --- دستور start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎵 سلام! آهنگ بفرست تا ذخیره بشه یا نامش رو جستجو کن.")

# --- دریافت آهنگ و ذخیره‌سازی ---
@bot.message_handler(content_types=['audio'])
def save_audio(message):
    songs = load_songs()
    song_id = message.audio.file_id
    title = message.audio.title or "بدون نام"
    songs[title] = song_id
    save_songs(songs)
    bot.reply_to(message, f"✅ آهنگ '{title}' ذخیره شد!")

# --- حالت Inline ---
@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_search(query):
    songs = load_songs()
    text = query.query.lower()
    results = []
    for title, file_id in songs.items():
        if text in title.lower():
            results.append(
                types.InlineQueryResultCachedAudio(
                    id=title,
                    audio_file_id=file_id,
                    title=title
                )
            )
    bot.answer_inline_query(query.id, results, cache_time=1)

# --- جستجو و ارسال آهنگ با تایپ مستقیم ---
@bot.message_handler(func=lambda message: True)
def send_song(message):
    songs = load_songs()
    text = message.text.lower()
    for title, file_id in songs.items():
        if text in title.lower():
            bot.send_audio(message.chat.id, file_id, caption=f"🎶 {title}")
            return
    bot.reply_to(message, "❌ آهنگی با این نام پیدا نشد.")

# --- اجرای ربات ---
print("✅ Bot is running...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
