from pathlib import Path
import vinca.card
from vinca.config import config

vinca_path = Path(__file__).parent
tags_path = vinca_path / 'tags'

class TagsCache(list):
	def __init__(self):
		self[:] = tags_path.read_text().splitlines()

	def update(self):
		'rebuild the tags list'
		all_cards = [vinca.card.Card(int(id.name)) for id in config.cards_path.iterdir()] 
		self[:] = [tag for card in all_cards for tag in card.tags]
		self.save()

	def save(self):
		tags_path.write_text('\n'.join(self))
	
	def add_tag(self, tag):
		if tag not in self:
			self.append(tag)
			self.save()

	def add_tags(self, tags):
		for tag in tags:
			self.add_tag(tag)

tags_cache = TagsCache()

	
		
