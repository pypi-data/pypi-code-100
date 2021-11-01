from services import translation_service
from tests import intruso_bot
intruso_bot.get_me().username
print(translation_service.get('START_COMMAND_BOT_ALREADY_STARTED_MESSAGE'))