import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from downloader import download_instagram_media
import file_manager
import os
import json

TOKEN = "7881556307:AAGr3krNZsuFV-6uCYrxtOV3qTSGODLicAU"
ADMIN_IDS = [5695870522, 6169032422]  # Admin ID larni shu yerga qo'shing
USERS_FILE = "users.json"
bot = telebot.TeleBot(TOKEN)

# "downloads" papkasini yaratish
os.makedirs("downloads", exist_ok=True)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return []

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

@bot.message_handler(commands=['start'])
def start_message(message):
    users = load_users()
    if message.chat.id not in users:
        users.append(message.chat.id)
        save_users(users)
    bot.send_message(message.chat.id, "Salom! Instagram video yoki rasm havolasini yuboring.")

@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = "\n".join([
        "📌 *Instagram Downloader Bot* foydalanish bo‘yicha yordam",
        "1️⃣ Instagram post havolasini yuboring.",
        "2️⃣ Bot rasm yoki videoni yuklab beradi.",
        "\n🚀 Tez, qulay va bepul!",
    ])
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['language'])
def language_message(message):
    markup = InlineKeyboardMarkup()
    languages = [
        ("🇺🇿 O‘zbek", "lang_uz"),
        ("🇬🇧 English", "lang_en"),
        ("🇷🇺 Русский", "lang_ru"),
        ("🇹🇷 Türkçe", "lang_tr"),
        ("🇫🇷 Français", "lang_fr"),
        ("🇩🇪 Deutsch", "lang_de"),
        ("🇪🇸 Español", "lang_es"),
        ("🇮🇹 Italiano", "lang_it"),
        ("🇨🇳 中文", "lang_zh"),
        ("🇯🇵 日本語", "lang_ja"),
        ("🇦🇪 العربية", "lang_ar"),
        ("🇮🇷 فارسی", "lang_fa"),
    ]
    for lang in languages:
        markup.add(InlineKeyboardButton(lang[0], callback_data=lang[1]))
    bot.send_message(message.chat.id, "Tilni tanlang / Choose a language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def handle_language_selection(call):
    lang_dict = {
        "uz": "Til O‘zbek tiliga o‘zgartirildi! 🇺🇿",
        "en": "Language changed to English! 🇬🇧",
        "ru": "Язык изменен на Русский! 🇷🇺",
        "tr": "Dil Türkçe olarak değiştirildi! 🇹🇷",
        "fr": "Langue changée en Français! 🇫🇷",
        "de": "Sprache auf Deutsch geändert! 🇩🇪",
        "es": "Idioma cambiado a Español! 🇪🇸",
        "it": "Lingua cambiata in Italiano! 🇮🇹",
        "zh": "语言更改为中文！🇨🇳",
        "ja": "言語が日本語に変更されました！🇯🇵",
        "ar": "تم تغيير اللغة إلى العربية! 🇦🇪",
        "fa": "زبان به فارسی تغییر یافت! 🇮🇷",
    }
    lang_code = call.data.split("_")[1]
    response = lang_dict.get(lang_code, "Til o‘zgartirilmadi.")
    bot.send_message(call.message.chat.id, response)

@bot.message_handler(commands=['myid'])
def myid_message(message):
    bot.send_message(message.chat.id, f"Sizning ID raqamingiz: {message.chat.id}")

@bot.message_handler(commands=['sendall'])
def sendall_message(message):
    if message.chat.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "⛔ Siz admin emassiz!")
        return
    
    text = message.text.replace("/sendall", "").strip()
    if not text:
        bot.send_message(message.chat.id, "Xabar matnini kiriting: /sendall [matn]")
        return
    
    users = load_users()
    for user_id in users:
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"Xatolik: {e}")
    
    bot.send_message(message.chat.id, "✅ Xabar barcha foydalanuvchilarga yuborildi.")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def handle_instagram_link(message):
    url = message.text
    bot.send_message(message.chat.id, "Yuklanmoqda...⏳")
    
    file_path, media_type = download_instagram_media(url)
    
    if not file_path or not os.path.exists(file_path):
        bot.send_message(message.chat.id, "Xatolik! Yuklangan fayl topilmadi.")
        return
    
    if media_type == "video":
        with open(file_path, 'rb') as video:
            bot.send_video(message.chat.id, video)
    elif media_type == "photo":
        with open(file_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    
    os.remove(file_path)

if __name__ == "__main__":
    bot.polling()
