from homebot.core.logging import LOGI
from homebot.lib.libadmin import user_is_approved
from homebot.modules.ci.manager import manager
from homebot.modules.ci.parser import CIParser
from telegram.ext import CallbackContext
from telegram.update import Update

def ci(update: Update, context: CallbackContext):
	if not user_is_approved(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to use CI function of this bot.\n"
								  "Ask to who host this bot to add you to the authorized people list")
		return

	parser = CIParser(prog="/ci")
	parser.set_output(update.message.reply_text)
	parser.add_argument('project', help='CI project',
						nargs='?', default=None,)
	parser.add_argument('-s', '--status',
						action='store_true', help='show queue status')

	args, project_args = parser.parse_known_args(context.args)

	if args.status:
		update.message.reply_text(manager.get_formatted_list())
		return

	if args.project is None:
		parser.error("Please specify a project")

	result = manager.add(args.project, update, context, project_args)
	text = result if result is not None else "Workflow added to the queue"

	update.message.reply_text(text)
	LOGI(text)
