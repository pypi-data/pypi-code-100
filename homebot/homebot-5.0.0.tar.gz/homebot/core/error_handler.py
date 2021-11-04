from homebot.core.logging import LOGE
from telegram.ext import CallbackContext
from telegram.update import Update
import traceback

def format_exception(exception):
	return ''.join(traceback.format_exception(type(exception), exception,
												   exception.__traceback__,
												   limit=None, chain=True))

def error_handler(update: Update, context: CallbackContext):
	formatted_error = ("HomeBot: Error encountered!\n"
	                   f"Command sent: {update.message.text}\n\n"
	                   f"{format_exception(context.error)}")
	LOGE(formatted_error)
	update.message.reply_text(formatted_error)
	LOGE("End error handling")
