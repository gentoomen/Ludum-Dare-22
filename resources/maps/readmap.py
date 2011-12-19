import json

class obj():
	def __init__(self, objfile=None, rot=None, scale=None, pos=None):
		self.objfile = objfile
		self.rotation = rot
		self.scale = scale
		self.position = pos

class GameMap():
	def parseFile(self, addr):
		f = open(addr,'r')
		line = f.read()
		f.close()
		content = json.JSONDecoder().decode(line)

		self.map = content['map']
		self.terrain = content['map']['terrain']['height']
		self.terraintex = content['map']['terrain']['texture']
		self.terraintexyreps = float(content['map']['terrain']['texturexreps'])
		self.terraintexxreps = float(content['map']['terrain']['textureyreps'])
		
		self.layout = content['map']['layout']

		self.schema = {}
		for i in content['map']['aliases']:
			f = open(i,'r')
			line = f.read()
			f.close()
			self.schema[i] = json.JSONDecoder().decode(line)

		self.objlist = []

		for alias in content['map']['aliases']:
			#print alias
			for mapobj in content['map']['layout']:
				self.objlist.append(obj(
				self.schema[alias]['objects'][mapobj['alias']],
				mapobj['rotation'],
				mapobj['scale'],
				mapobj['position']
				))