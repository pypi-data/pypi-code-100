from .exceptions import APIError
from .games import Bedwars
from .profile import *





class Player:

	def __init__(self, data):

		self.data = data
		self.name = self.data.get("player", {}).get("displayname")
		self.uuid = self.data.get("player", {}).get("uuid")
		self.rank = Rank(data)
		self.bedwars = Bedwars(data)