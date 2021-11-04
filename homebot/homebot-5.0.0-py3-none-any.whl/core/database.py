import json
from pathlib import Path
from threading import Lock

DATABASE_FILE_NAME = "data.json"

ALLOWED_DATA_TYPES = [
	bool,
	dict,
	float,
	int,
	list,
	# TODO: With 3.10 move to types.NoneType
	type(None),
	str,
]

class HomeBotDatabase:
	def __init__(self):
		"""Initialize the database."""
		self.dict = {}
		self.file_path = Path(DATABASE_FILE_NAME)
		self.data_lock = Lock()
		self.file_lock = Lock()

		if self.file_path.is_file():
			self._load()

		self._dump()

	def get(self, k: str):
		if type(k) is not str:
			raise TypeError("Key isn't a string")

		with self.data_lock:
			if not '.' in k:
				value = self.dict[k]
			else:
				value = dict(self.dict)
				for subkey in k.split('.'):
					value = value[subkey]

			return value

	def set(self, k: str, v):
		if type(k) is not str:
			raise TypeError("Key isn't a string")

		if type(v) not in ALLOWED_DATA_TYPES:
			raise TypeError("Value data type not allowed")

		with self.data_lock:
			if not '.' in k:
				self.dict[k] = v
			else:
				d = v
				for subkey in k.split('.')[::-1]:
					d = {subkey: d}

				self.dict.update(d)

			self._dump()

	def _load(self):
		with self.file_lock:
			self.dict.update(json.loads(self.file_path.read_bytes()))

	def _dump(self):
		with self.file_lock:
			self.file_path.write_text(json.dumps(self.dict, indent=4, sort_keys=True))

# Only one database is allowed for now
# TODO: Set custom names for bot instances and
# allow to have one database per bot
database = HomeBotDatabase()
