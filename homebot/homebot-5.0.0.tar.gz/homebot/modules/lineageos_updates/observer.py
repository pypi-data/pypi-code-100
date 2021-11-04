from datetime import datetime
from homebot.modules.lineageos_updates.device_data import get_device_updates
from homebot.core.logging import LOGE, LOGI
from homebot.core.config import get_config
from threading import Event, Thread
from time import sleep

API_URL = "https://download.lineageos.org/api/v1/{device}/nightly/1"

class Observer:
	def __init__(self):
		self.devices = get_config("lineageos_updates.devices", [])
		self.last_device_post = {}
		self.posters = {}

		now = int(datetime.now().timestamp())
		for device in self.devices:
			self.last_device_post[device] = now

		self.event = Event()
		if get_config("lineageos_updates.enable", False) and self.devices:
			self.event.set()

		self.thread = Thread(target=self.daemon, name="LineageOS updates observer", daemon=True)
		self.thread.start()

	def daemon(self):
		while True:
			self.event.wait()
			for device in self.devices:
				try:
					response = get_device_updates(device)
				except Exception:
					response = {}

				if not response:
					continue

				last_update = response[-1]

				build_date = last_update["datetime"]
				if build_date <= self.last_device_post[device]:
					continue

				self.last_device_post[device] = build_date

				for poster in self.posters.values():
					try:
						poster.post(device, build_date, last_update["version"])
					except Exception:
						LOGE(f"Failed to post {device} {build_date} build")
					else:
						LOGI(f"Build {device} {build_date} posted successfully")

			# Wait 10 minutes
			sleep(10 * 60)
