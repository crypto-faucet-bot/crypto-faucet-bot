import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Подключение к базе
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, referred_by INTEGER)")

# Загрузка кранов
with open("faucets.json", "r", encoding="utf-8") as f:
    faucets = json.load(f)

# Команда /start
@bot.message_handler(commands=["start"])
def start_handler(message):
    ref = message.text.split()[1] if len(message.text.split()) > 1 else None
    user_id = message.from_user.id

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id, referred_by) VALUES (?, ?)", (user_id, ref))
        conn.commit()

    bot.send_message(user_id, "👋 Добро пожаловать в крипто-кран бот!")
    show_menu(user_id)

# Главное меню
def show_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📋 Краны", callback_data="faucets"))
    markup.add(InlineKeyboardButton("👥 Рефералы", callback_data="ref"))
    bot.send_message(chat_id, "Выберите опцию:", reply_markup=markup)

# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "faucets":
        text = "🧴 Список кранов:\n\n"
        for f in faucets:
            text += f"🔹 <b>{f['name']}</b> — <a href=\"{f['link']}\">Перейти</a>\n"
        bot.send_message(call.message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True)
    elif call.data == "ref":
        user_id = call.from_user.id
        cursor.execute("SELECT COUNT(*) FROM users WHERE referred_by=?", (user_id,))
        count = cursor.fetchone()[0]
        username = bot.get_me().username
        referral_text = (
            f"👥 У вас {count} рефералов\n"
            f"🔗 Ваша ссылка:\n"
            f"https://t.me/{username}?start={user_id}"
        )
        bot.send_message(user_id, referral_text)

# Запуск
bot.infinity_polling()
