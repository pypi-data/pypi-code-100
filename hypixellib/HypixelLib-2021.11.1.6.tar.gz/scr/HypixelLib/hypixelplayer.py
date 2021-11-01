from .exceptions import APIError
from .games import Bedwars
from .profile import *





class Player:

	def __init__(self, data):

		self.data = data

		self.name = self.data.get("player", {}).get("displayname")
		self.uuid = self.data.get("player", {}).get("uuid")


		#Network statistics, like rank, karma, level, ...
		self.rank = Rank(data)
		self.karma = self.data.get("player", {}).get("karma")
		self.network_experience = self.data.get("player", {}).get("networkExp")
		self.network_level = network_level = round((math.sqrt((2 * network_experience) + 30625) / 50) - 2.5, 2)
		
		#Game statistics
		self.bedwars = Bedwars(data)