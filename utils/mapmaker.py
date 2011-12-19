import pygame
import json
import sys
from decimal import *


if len(sys.argv) != 3:
	print "Usage: mapmaker.py WIDTH HEIGHT"
	print "Left mouse to lower the map point"
	print "Right mouse to raise the map point"
	exit()

pygame.init()

lock = False

font = pygame.font.SysFont(pygame.font.get_default_font(), 12)

class tile():
	def __init__(self, x=None, y=None, h=None):
		self.x = x
		self.y = y
		self.h = h
		self.color = (100,255,100)
	def up(self):
		if self.h < 0.9:
			self.h += 0.1
			self.color = (self.color[0]+10,255,self.color[0]+10)
	def down(self):
		if self.h > -0.9:
			self.h -= 0.1
			self.color = (self.color[0]-10,255,self.color[0]-10)
	def reset(self):
		self.h = 0.0
	def display(self, surface):
		rc = (self.x*16, self.y*16, self.x+16, self.y+16)
		pygame.draw.rect(surface,self.color, rc)
		temp = font.render(str(float(Decimal(self.h).quantize(Decimal('.1')))),0,(0,0,0))
		screen.blit(temp,(self.x*16,self.y*16))

width, height = (int(sys.argv[1])*16, int(sys.argv[2])*16)
screen = pygame.display.set_mode((width, height+30))

tiles = []
for y in range(0,height/16):
	tmp = []
	for x in range(0,width/16):
		tmp.append(tile(x,y,0.0))
	tiles.append(tmp)

while True:
	screen.fill((0,0,0)) #Filling with black

	for y in tiles:
		for x in y:
			x.display(screen)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN and lock == False:
			pos = pygame.mouse.get_pos()
			lock = True
			if event.button == 1:
				i = tiles[pos[1]/16][pos[0]/16]
				i.down()
				lock = False
			elif event.button == 3:
				i = tiles[pos[1]/16][pos[0]/16]
				i.up()
				lock = False
		key=pygame.key.get_pressed()
		if key[pygame.K_SPACE]:
			m = []
			for y in tiles:
				tmp = []
				for x in y:
					tmp.append(float(Decimal(x.h).quantize(Decimal('.1'))))
				m.append(tmp)
			print json.dumps(m)

	temp = font.render(str("M1 TO DROP, M2 TO RAISE"),1,(0,0,0))

	screen.blit(temp,(5,height+20))
	pygame.display.flip()