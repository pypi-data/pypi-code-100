import json

class BaseSerializable:
	basicTypes = [str, int, float, bool]

	def toJson(self, indent=None):
		'''Convert to JSON'''
		return json.dumps(self.toDict(), indent=indent)

	def toDict(self):
		'''Internal use method'''
		diccionario = {}
		for attr, value in self.__dict__.items():
			tipo = type(self.__dict__.get(attr))

			if tipo in self.basicTypes:
				diccionario[attr] = value
			elif tipo == list:
				diccionario[attr] = list(map(self.toDictLista,value))
			else:
				diccionario[attr] = self.__dict__.get(attr).toDict()
		return diccionario

	def toDictLista(self, itemDeLaLista):
		'''Internal use method'''
		tipo = type(itemDeLaLista)
		if tipo in self.basicTypes:
			return itemDeLaLista
		elif tipo == list:
			return list(map(self.toDictLista, itemDeLaLista))
		else:
			return itemDeLaLista.toDict()
