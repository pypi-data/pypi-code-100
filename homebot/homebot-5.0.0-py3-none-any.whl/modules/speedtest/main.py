from datetime import datetime
from homebot.core.logging import LOGI
from speedtest import Speedtest
from telegram.ext import CallbackContext
from telegram.update import Update
from threading import Lock

class SpeedtestResult:
	def __init__(self):
		self.date: datetime = None
		self.download: str = None
		self.upload: str = None
		self.lock = Lock()

	def set_data(self, date, download, upload):
		with self.lock:
			self.date: datetime = date
			self.download: str = download
			self.upload: str = upload

last_speedtest = SpeedtestResult()

def speedtest(update: Update, context: CallbackContext):
	now = datetime.now()
	# Use cached values if < 5 minutes
	if last_speedtest.date is not None and (now - last_speedtest.date).seconds < 5 * 60:
		update.message.reply_text(f"Download: {last_speedtest.download} mbps\n"
								  f"Upload: {last_speedtest.upload} mbps\n"
								  f"Cached results from {last_speedtest.date.strftime('%m/%d/%Y, %H:%M:%S')}")
		return
	message_id = update.message.reply_text("Running speedtest...").message_id
	LOGI("Started")
	speedtest = Speedtest()
	speedtest.get_best_server()
	speedtest.download()
	speedtest.upload()
	speedtest.results.share()
	results_dict = speedtest.results.dict()
	download = str(results_dict["download"] // 10 ** 6)
	upload = str(results_dict["upload"] // 10 ** 6)
	last_speedtest.set_data(now, download, upload)
	context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=message_id,
								  text=f"Download: {download} mbps\n"
									   f"Upload: {upload} mbps")
	LOGI(f"Finished, download: {download} mbps, upload: {upload} mbps")
