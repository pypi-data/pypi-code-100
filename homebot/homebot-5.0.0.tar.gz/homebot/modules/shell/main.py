from homebot.lib.libadmin import user_is_admin
import subprocess
from telegram.constants import MAX_MESSAGE_LENGTH, PARSEMODE_HTML
from telegram.ext import CallbackContext
from telegram.update import Update
from tempfile import TemporaryFile

def shell(update: Update, context: CallbackContext):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to use the shell")
		return

	if len(update.message.text.split(' ', 1)) < 2:
		update.message.reply_text("No command provided")
		return

	command = update.message.text.split(' ', 1)[1]
	try:
		process = subprocess.check_output(command, shell=True, executable="/bin/bash",
										  stderr=subprocess.STDOUT, universal_newlines=True,
										  encoding="utf-8")
	except subprocess.CalledProcessError as e:
		returncode = e.returncode
		output = e.output
	else:
		returncode = 0
		output = process

	text = (
		f"Command: <pre>{command}</pre>\n"
		f"Return code: {returncode}\n"
		"\n"
	)

	text_message = (
		"Output:\n"
		f"<pre>{output}</pre>"
	)

	text_document = "Output: sent as document"

	if len(text) + len(text_message) < MAX_MESSAGE_LENGTH:
		text += text_message
		update.message.reply_text(text, parse_mode=PARSEMODE_HTML)
	else:
		text += text_document
		fd = TemporaryFile(mode='r+')
		fd.write(output)
		fd.seek(0)
		update.message.reply_document(document=fd, filename="output.txt",
		                              caption=text, parse_mode=PARSEMODE_HTML)
		fd.close()
