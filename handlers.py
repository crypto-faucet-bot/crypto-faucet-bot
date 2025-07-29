from aiogram import types, Dispatcher
import json
from database import init_db, register_user, get_referral_stats

async def start_handler(message: types.Message):
    await init_db()
    user_id = message.from_user.id
    username = message.from_user.username
    ref_id = message.get_args()
    if ref_id.isdigit() and int(ref_id) != user_id:
        await register_user(user_id, username, int(ref_id))
    else:
        await register_user(user_id, username)

    await message.answer("👋 Привет! Добро пожаловать в CryptoRainBot.\n\n🪙 Напиши /faucets чтобы посмотреть доступные краны.")

async def faucets_handler(message: types.Message):
    with open("faucets.json", "r", encoding="utf-8") as f:
        faucets = json.load(f)

    text = "🪙 *Краны для заработка крипты:*\n\n"
    for faucet in faucets:
        text += (
            f"🔹 *{faucet['name']}*\n"
            f"💰 Монета: {faucet['coin']}\n"
            f"⏱ Интервал: {faucet['interval']}\n"
            f"🛡️ Защита: {faucet['protection']}\n"
            f"🔗 [Перейти]({faucet['url']})\n\n"
        )
    await message.answer(text, parse_mode="Markdown")

async def stats_handler(message: types.Message):
    count = await get_referral_stats(message.from_user.id)
    await message.answer(f"📊 У тебя {count} реферал(ов).\nТвоя ссылка: https://t.me/{message.bot.username}?start={message.from_user.id}")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(faucets_handler, commands=["faucets"])
    dp.register_message_handler(stats_handler, commands=["stats"])