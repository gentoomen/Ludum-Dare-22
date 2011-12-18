import json

class obj():
	def __init__(self, objfile=None):
		self.objfile = objfile

class GameMap():
	def parseFile(self, addr):
		f = open(addr,'r')
		str = f.read()
		f.close()
		content = json.JSONDecoder().decode(str)

		self.map = content['map']
		self.terrain = content['map']['terrain']
		self.layout = content['map']['layout']

		self.schema = []
		for i in content['map']['aliases']:
			f = open(i,'r')
			str = f.read()
			f.close()
			self.schema.append(json.JSONDecoder().decode(str))

		self.objlist = []
		for k in content['map']['layout'].keys():
			self.objlist.append(obj(self.schema['objects'][k]))
