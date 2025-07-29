import logging
from aiogram import Bot, Dispatcher, executor, types
from handlers import register_handlers
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)