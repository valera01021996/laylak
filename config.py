from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv("BOT_TOKEN"))


ADMINS = ["43031788", "-4197023200"]

dp = Dispatcher(bot, storage=storage)
