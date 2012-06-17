import pygame, utils
from pygame.locals import *

# Should look at pygame docs and examples of 
# sprite sheet use with built in sprite classes.
# Current implementation could probably do without
# inheriting from DirtySprite

class IcySprite(pygame.sprite.DirtySprite):
	def __init__(self, rect, sheet, area = (0,0,0,0)):
		pygame.sprite.DirtySprite.__init__(self)
		self.area = area
		self.rect = pygame.Rect(rect)
		self.dirty = 1
		self.sheet = sheet
	# Used by wrapper.Stage
	def draw(self, surface):
		if self.dirty == 1:
			surface.blit(self.sheet, self.rect, self.area)
			self.dirty = 0

# Player character class
class Protagonist(IcySprite):
	def __init__(self, rect, sheet, area = (0,0,16,16)):
		IcySprite.__init__(self, rect, sheet, area)
		self.xVel, self.yVel = 0, 0
		self.oldXVel, self.oldYVel = 0, 0
		self.health = 100
		# | Fixes bug where character isn't drawn when game starts
		# V until the user presses an arrow key
		self.needsInitialDraw = True
	def update(self):
		# Key states for player movement
		# Maybe use events, this isn't working perfectly
		keyPressed = pygame.key.get_pressed()
		if keyPressed[K_UP]: 
			self.yVel -= 4
			self.xVel = 0
		if keyPressed[K_DOWN]: 
			self.yVel += 4
			self.xVel = 0
		if keyPressed[K_RIGHT]: 
			self.xVel += 4
			self.yVel = 0
		if keyPressed[K_LEFT]: 
			self.xVel -= 4
			self.yVel = 0
		if not self.needsInitialDraw and self.xVel == 0 and self.yVel == 0:
			self.dirty = 0
			return
		self.dirty = 1
		newX = self.rect[0] + self.xVel
		newY = self.rect[1] + self.yVel
		self.rect = (newX, newY, self.rect[2], self.rect[3])
		# Update old (previous frame) velocities
		self.oldXVel = self.xVel
		self.oldYVel = self.yVel
		self.xVel = self.yVel = 0
	
# Tile class: super class for objects sharing the simple_tileset.png file
class Tile(IcySprite):
	def __init__(self, rect, sheet, area = (0,0,0,0)):
		IcySprite.__init__(self, rect, sheet, area)
	def update(self):
		pass
		
class GrassTile(Tile):
	def __init__(self, rect, sheet, area = (0,0,16,16)):
		Tile.__init__(self, rect, sheet, area)
		
class RoadTile(Tile):
	def __init__(self, rect, sheet, area = (16,0,16,16)):
		Tile.__init__(self, rect, sheet, area)
	
class BlockTile(Tile):
	def __init__(self, rect, sheet, area = (48,0,16,16)):
		Tile.__init__(self, rect, sheet, area)
