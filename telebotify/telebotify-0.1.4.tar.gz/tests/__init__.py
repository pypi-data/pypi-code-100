import os

from dotenv import load_dotenv

load_dotenv()

from bot_base import Bot

intruso_bot = Bot(os.environ["BOT_KEY"])
