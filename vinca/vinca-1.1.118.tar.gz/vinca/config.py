import json
from pathlib import Path

# so far the config object only stores the path
# in which to look for cards
class Config(dict):
	path = Path(__file__).parent / 'config.json'
	
	def __init__(self):
		dict.__init__(self, self.load())
	
	def load(self):
		with open(self.path) as f:
			return json.load(f)

	def save(self):
		with open(self.path,'w') as f:
			json.dump(self, f)

	def set_cards_path(self, path):
		self['cards_path'] = path
		self.save()

	@property
	def cards_path(self):
		return Path(self['cards_path'])

config = Config()
