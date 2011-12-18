import pygame

class SoundEngine():
	def __init__(self):
		pygame.mixer.init()
		self.library = {}

	def addTrack(self, songname):
		if songname not in self.library.keys():
			song = pygame.mixer.Sound(songname)
			self.library[songname] = song

	def playTrack(self, songname, time=None, loop=0):
		if songname in self.library.keys():
			if time == None:
				time = self.lenTrack(songname)*1000
			self.library[songname].play(maxtime=int(time),loops=loop)
	
	def stopTrack(self, songname, fadeout=False):
		if songname in self.library.keys():
			if fadeout == False:
				self.library[songname].stop()
			else:
				self.library[songname].fadeout()

	'''Returns the length of the song in seconds'''
	def lenTrack(self, songname):
		if songname in self.library.keys():
			return self.library[songname].get_length()

	def setVolume(self, songname, volume=.5):
		self.library[songname].set_volume(volume)
