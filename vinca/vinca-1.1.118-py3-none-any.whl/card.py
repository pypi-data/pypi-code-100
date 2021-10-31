import subprocess
import json
import datetime
TODAY = datetime.date.today()
from pathlib import Path

from vinca import reviewers, editors, schedulers 
from vinca.tag_caching import tags_cache
from vinca.config import config
from vinca.lib.fancy_input import fancy_input

class Card:
	# Card class can load without 
	default_metadata = {'editor': 'base', 'reviewer':'base', 'scheduler':'base',
			    'tags': [], 'history': [[TODAY, 0, 'create']], 'deleted': False,
			    'due_date': TODAY, 'string': ''}

	def __init__(self, id=None, create=False):
		assert isinstance(id, int) ^ create
		if not create:
			self.init_loaded_card(id)
		elif create:
			self.init_new_card()
		self._hotkeys = {'e': self.edit,
				'E': self.edit_metadata,
				'M': self.print_metadata,
				't': self.edit_tags,
				'd': self.delete,
				's': self.summarize,
				'r': self.review}
		self._confirm_exit_commands = [self.print_metadata, self.summarize]



	def init_loaded_card(self, id):
		self.id = id
		self.metadata_is_loaded = False

	def init_new_card(self):
		old_cids = [int(x.name) for x in config.cards_path.iterdir()]
		self.id = max(old_cids) + 1 if old_cids else 100 
		self.path.mkdir()
		self.metadata = Card.default_metadata
		self.metadata_is_loaded = True
		self.save_metadata()

	def summarize(self):
		s = f'id\t{self.id}\n'
		s += f'due\t{self.due_date}\n'
		s += f'seen\t{len(self.history)}\n'
		s += f'time\t{self.total_time}s\n'
		print(s)

	@property
	def path(self):
		return config.cards_path/str(self.id)

	@property
	def metadata_path(self):
		return self.path / 'metadata.json'

	def load_metadata(self):
		self.metadata = json.load(self.metadata_path.open())
		# dates must be serialized into strings for json
		# I unpack them here
		str_to_date = datetime.date.fromisoformat
		self.metadata['history'] = [[str_to_date(date), grade,
					    time] for date, grade, time in self.metadata['history']]
		assert self.metadata['history'], f'empty history metadata for {self.path}'
		self.metadata['due_date'] = str_to_date(self.metadata['due_date'])
		self.metadata_is_loaded = True

	def save_metadata(self):
		json.dump(self.metadata, self.metadata_path.open('w'), default=str, indent=2)

	for m in default_metadata.keys():
		# create getter and setter methods for everything in the metadata dictionary
		exec(f'''
@property
def {m}(self):
	if not self.metadata_is_loaded:
		self.load_metadata()
	return self.metadata["{m}"]''')
		exec(f'''
@{m}.setter
def {m}(self, new_val):
	if not self.metadata_is_loaded:
		self.load_metadata()
	self.metadata["{m}"] = new_val
	self.save_metadata()''')	

	# overwrite the tags setter with one modification
	# we want to update the tags_cache
	@tags.setter
	def tags(self, tags):
		if not self.metadata_is_loaded:
			self.load_metadata()
		self.metadata['tags'] = tags
		self.save_metadata()
		tags_cache.add_tags(tags)

	# overwrite the due-date setter with one modification
	# we want to move the card's path to facilitate caching
	# TODO

	def __str__(self):
		return self.string

	def add_history(self, date, time, grade):
		self.history = self.history + [[date, time, grade]]
			
	def review(self): reviewers.review(self)
	def make_string(self): self.string = reviewers.make_string(self)
	def edit(self):
		editors.edit(self) 
		self.make_string()
	def edit_metadata(self):
		subprocess.run(['vim',self.path/'metadata.json'])
		self.load_metadata()
		self.make_string()
	def print_metadata(self):
		for k,v in self.metadata.items():
			print(f'{k:20}',v,end='\n\n')
	def schedule(self): schedulers.schedule(self) 

	def delete(self, toggle=True):
		if toggle:
			self.deleted = not self.deleted
		elif not toggle:
			self.deleted = True

		

	@property
	def create_date(self): return self.history[0][0] if self.history else None
	@property
	def seen_date(self): return self.history[-1][0] if self.history else None
	@property
	def last_grade(self): return self.history[-1][2] if self.history else None
	@property
	def last_interval(self): return self.history[-1][0] - self.history[-2][0] if len(self.history)>1 else None


	@property
	def total_time(self):
		return sum([time for date,time,grade in self.history])

	@property
	def new(self): return self.last_grade == 'create'

	def due_as_of(self, date):
		return self.due_date <= date

	@property
	def is_due(self): return self.due_as_of(TODAY)

	def edit_tags(self):
		self.tags = fancy_input(prompt = 'tags: ', text = ' '.join(self.tags), completions = tags_cache).split()
