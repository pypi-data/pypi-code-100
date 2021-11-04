from calendar import day_name
from datetime import datetime
from homebot.lib.libadmin import user_is_admin
from homebot.modules.lineageos_updates.device_data import get_device_updates
from homebot.modules.lineageos_updates.observer import Observer
from homebot.modules.lineageos_updates.poster import Poster
from shutil import which
from subprocess import check_output
from telegram.bot import Bot
from telegram.ext import CallbackContext
from telegram.update import Update
from typing import Callable

_observer = Observer()

def add_user(self, bot: Bot):
	_observer.posters[bot] = Poster(bot)

def remove_user(self, bot: Bot):
	if bot in _observer.posters:
		del _observer.posters[bot]

def disable(update: Update, context: CallbackContext):
	_observer.event.clear()
	update.message.reply_text("Observer disabled")

def enable(update: Update, context: CallbackContext):
	_observer.event.set()
	update.message.reply_text("Observer enabled")

def info(update: Update, context: CallbackContext):
	alive = _observer.thread.is_alive()
	text = f"Enabled: {str(alive)}\n"
	if alive:
		text += (
			"Observed devices:\n"
			"Device | Last post\n"
		)
		for device in _observer.last_device_post:
			date = datetime.fromtimestamp(_observer.last_device_post[device])
			text += f"{device} | {date.strftime('%Y/%m/%d, %H:%M:%S')}\n"

	update.message.reply_text(text)

def last(update: Update, context: CallbackContext):
	if len(context.args) < 2:
		update.message.reply_text("Device codename not specified")
		return

	device = context.args[1]
	response = get_device_updates(device)
	if not response:
		update.message.reply_text(f"Error: no updates found for {device}")
		return

	last_update = response[-1]
	update.message.reply_text(f"Last update for {device}:\n"
	                          f"Filename: {last_update['filename']}\n"
	                          f"Version: {last_update['version']}\n"
	                          f"Download: {last_update['url']}")

def when(update: Update, context: CallbackContext):
	if len(context.args) < 2:
		update.message.reply_text("Device codename not specified")
		return

	if which("python2") is None:
		update.message.reply_text("Python 2.x isn't installed, it's required to parse the day")
		return

	device = context.args[1]
	command = f'from random import Random; print(Random("{device}").randint(1, 7))'
	day_int = int(check_output(f"python2 -c '{command}'", shell=True))
	day = day_name[day_int - 1]
	update.message.reply_text(f"The next build for {device} will be on {day}")

# name: [function, admin_only]
COMMANDS: dict[str, list[Callable[[Update, CallbackContext], None], bool]] = {
	"disable": [disable, True],
	"enable": [enable, True],
	"info": [info, False],
	"last": [last, False],
	"when": [when, False],
}

HELP_TEXT = (
	"Available commands:\n" +
	"\n".join(COMMANDS.keys())
)

def lineageos_updates(update: Update, context: CallbackContext):
	if not context.args:
		update.message.reply_text(
			"Error: No argument provided\n\n"
			f"{HELP_TEXT}"
		)
		return

	command = context.args[0]

	if command not in COMMANDS:
		update.message.reply_text(
			f"Error: Unknown command {command}\n\n"
			f"{HELP_TEXT}"
		)
		return

	func, admin_only = COMMANDS[command]

	if admin_only and not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to use this function")
		return

	func(update, context)
