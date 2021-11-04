from homebot.modules.xda.words import WORDS
import random
from telegram.ext import CallbackContext
from telegram.update import Update

def xda(update: Update, context: CallbackContext):
	length = random.randint(3, 10)
	string = random.choices(list(WORDS.keys()), weights=list(WORDS.values()), k=length)
	random.shuffle(string)
	update.message.reply_text(" ".join(string))
