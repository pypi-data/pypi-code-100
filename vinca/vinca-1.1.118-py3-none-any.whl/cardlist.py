import re
import datetime
from shutil import copytree, rmtree
from pathlib import Path
from vinca.browser import Browser
from vinca.lib import ansi
from vinca.lib.fancy_input import fancy_input
from vinca.lib.readkey import readkey
from vinca.lib import casting
from vinca.config import config
from vinca.tag_caching import tags_cache
TODAY = datetime.date.today()
DAY = datetime.timedelta(days = 1)

class Cardlist:
	''' this is a collection of cards. most of the user interface takes place through the browser '''


	def __init__(self, _cards):
		# we do not subclass list so that
		# the fire help is not littered
		# with inherited methods
		self._cards = _cards
		self._hotkeys = {'D': self.delete,
				 'T': self.edit_tags,
				 'C': self.count}
		self._confirm_exit_commands = [self.count]

	def __iter__(self):
		return iter(self._cards)

	def __len__(self):
		return len(self._cards)

	def __getitem__(self, slice):
		return self._cards[slice]

	def insert(self, idx, obj):
		self._cards.insert(idx, obj)

	def __str__(self):
		s = ''
		l = len(self)
		if l == 0:
			return 'No cards.'
		if l > 10:
			s += f'10 of {l}\n'
		s += ansi.codes['line_wrap_off']
		for card in self[:10]:
			if card.due_as_of(TODAY):
				s += ansi.codes['bold']
				s += ansi.codes['blue']
			if card.deleted:
				s += ansi.codes['crossout']
				s += ansi.codes['red']
			s += f'{card.id}\t{card}\n'
			s += ansi.codes['reset']
		s += ansi.codes['line_wrap_on']
		return s

	def browse(self):
		''' scroll through your collection with j and k '''
		Browser(self).browse()
	b = browse

	def review(self):
		''' review all cards '''
		Browser(self).review()
	r = review
				
	def add_tag(self, tag):
		for card in self:
			card.tags += [tag]

	def remove_tag(self, tag):
		for card in self:
			if tag in card.tags:
				card.tags.remove(tag)
			# TODO do this with set removal
			card.save_metadata()

	def count(self):
		''' simple summary statistics '''
		total_count = len(self)
		new_count = len(self.filter(new_only=True))
		due_count = len(self.filter(due_only=True))
		print('total',total_count,sep='\t')
		print('new',new_count,sep='\t')
		print('due',due_count,sep='\t')

	def edit_tags(self):
		tags_add = fancy_input(prompt = 'tags to add: ', completions = tags_cache).split()
		tags_remove = fancy_input(prompt = 'tags to remove: ', completions = tags_cache).split()
		for tag in tags_add:
			self.add_tag(tag)
		for tag in tags_remove:
			self.remove_tag(tag)

	def save(self, save_path):
		''' backup your cards '''
		save_path = casting.to_path(save_path)
		for card in self:
			copytree(card.path, save_path / str(card.id))

	@staticmethod
	def load(load_path, overwrite = False):
		load_path = casting.to_path(load_path)
		if overwrite:
			rmtree(config.cards_path)
			copytree(load_path, config.cards_path)
			return
		old_ids = [card.id for card in ALL_CARDS]
		max_old_id = max(old_ids, default = 1)
		for new_id,card_path in enumerate(load_path.iterdir(), max_old_id + 1):
			copytree(card_path, config.cards_path / str(new_id))


	def purge(self):
		''' Permanently delete all cards marked for deletion. '''
		deleted_cards = self.filter(deleted_only = True)
		if not deleted_cards:
			print('no cards are marked for deletion.')
			return
		print(f'delete {len(deleted_cards)} cards? (y/n)')
		if (confirmation := readkey()) == 'y':
			for card in deleted_cards:
				rmtree(card.path)

	def delete(self):
		for card in self:
			card.delete(toggle = True)



	def filter(self, pattern='', 
		   tags_include={}, tags_exclude={}, # specify a SET of tags
		   create_date_min=None, create_date_max=None,
		   seen_date_min=None, seen_date_max=None,
		   due_date_min=None, due_date_max=None,
		   editor=None, reviewer=None, scheduler=None,
		   deleted_only=False, 
		   due_only=False,
		   new_only=False,
		   invert=False):
		''' try --due_only or --pattern='Gettysburg Address' '''
		
		# cast dates to dates
		create_date_min = casting.to_date(create_date_min)
		create_date_max = casting.to_date(create_date_max)
		seen_date_min = casting.to_date(seen_date_min)
		seen_date_max = casting.to_date(seen_date_max)
		due_date_min = casting.to_date(due_date_min)
		due_date_max = casting.to_date(due_date_max)

		if due_only: due_date_max = TODAY
		# compile the regex pattern for faster searching
		p = re.compile(f'({pattern})')  # wrap in parens to create regex group \1

		tags_include, tags_exclude = set(tags_include), set(tags_exclude)

		f = lambda card: (((not tags_include or bool(tags_include & set(card.tags))) and
				(not tags_exclude or not bool(tags_exclude & set(card.tags))) and
				(not create_date_min or create_date_min <= card.create_date) and
				(not create_date_max or create_date_max >= card.create_date) and 
				(not seen_date_min or seen_date_min <= card.seen_date) and
				(not seen_date_max or seen_date_max >= card.seen_date) and 
				(not due_date_min or due_date_min <= card.due_date) and
				(not due_date_max or due_date_max >= card.due_date) and 
				(not editor or editor == card.editor) and
				(not reviewer or reviewer == card.reviewer) and
				(not scheduler or scheduler == card.scheduler) and
				(not deleted_only or card.deleted ) and
				(not new_only or card.new) and
				(not pattern or bool(p.search(card.string)))) != 
				invert)
		
		# matches.sort(key=lambda card: card.seen_date, reverse=True)
		return self.__class__([c for c in self if f(c)])
	f = filter

	def sort(self, create_date=False, seen_date=False, due_date=False, reverse=False):
		''' sort the collection '''
		if create_date:
			return self.__class__(sorted(self,
				key=lambda card: card.create_date, reverse=not reverse))
		if seen_date:
			return self.__class__(sorted(self,
				key=lambda card: card.seen_date, reverse=not reverse))
		if due_date:
			return self.__class__(sorted(self,
				key=lambda card: card.due_date, reverse=reverse))
		print('supply a criterion: --create_date | --seen_date | --due_date')
	s = sort
	

