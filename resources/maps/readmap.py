import json

class obj():
	def __init__(self, objfile=None):
		self.objfile = objfile
		#other shit can go here too, this is just to test

class GameMap():
	def parseFile(self, addr):
		f = open(addr,'r')
		str = f.read()
		f.close()
		content = json.JSONDecoder().decode(str)

		self.map = content['map']
		self.terrain = content['map']['terrain']
		self.layout = content['map']['layout']

		self.schema = {}
		for i in content['map']['aliases']:
			f = open(i,'r')
			str = f.read()
			f.close()
			self.schema[i] = json.JSONDecoder().decode(str)

		self.objlist = []

		for alias in content['map']['aliases']:
			for mapobj in content['map']['layout']:
				self.objlist.append(obj(self.schema[alias]['objects'][mapobj]))