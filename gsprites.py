import pygame
from pygame.locals import *

# Should look at pygame docs and examples of 
# sprite sheet use with built in sprite classes.
# Current implementation could probably do without
# inheriting from DirtySprite

# Constant defining number of times to scale2x the game
ZOOM_LVL = 1
def rectZoom(rect):
	for i in range(ZOOM_LVL):
		rect = (rect[0]*2,rect[1]*2,rect[2]*2,rect[3]*2)
	return rect
		
class IcySprite(pygame.sprite.DirtySprite):
	def __init__(self, rect, sheet, area = (0,0,0,0)):
		pygame.sprite.DirtySprite.__init__(self)
		self.area = pygame.Rect(rectZoom(area))
		self.rect = pygame.Rect(rectZoom(rect))
		self.dirty = 1
		self.sheet = sheet
	# Used by wrapper.Stage
	def draw(self, surface):
		if self.dirty == 1:
			surface.blit(self.sheet, self.rect, self.area)
			self.dirty = 0

# Player character class
class Protagonist(IcySprite):
	# Constants for use by Protagonist class
	NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
	FRAMES_PER_STILL = 4
	def __init__(self, rect, sheet, area = (0,0,16,16)):
		IcySprite.__init__(self, rect, sheet, area)
		self.xVel, self.yVel = 0, 0
		self.oldXVel, self.oldYVel = 0, 0
		self.health = 100
		self.dir = Protagonist.SOUTH
		self.frame = 0
		self.frameChangeCount = 0
		# | Fixes bug where character isn't drawn when game starts
		# V until the user presses an arrow key
		self.needsInitialDraw = True
	def update(self):
		# Key states for player movement
		# Maybe use events in addition, this isn't working perfectly
		keyPressed = pygame.key.get_pressed()
		if keyPressed[K_UP]:
			self.dir = Protagonist.NORTH 
			self.yVel -= 4
		if keyPressed[K_DOWN]: 
			self.dir = Protagonist.SOUTH
			self.yVel += 4
		if keyPressed[K_RIGHT]: 
			self.dir = Protagonist.EAST
			self.xVel += 4
		if keyPressed[K_LEFT]:
			self.dir = Protagonist.WEST 
			self.xVel -= 4
		if (not self.needsInitialDraw) and self.xVel == 0 and self.yVel == 0:
			self.dirty = 0
			return
		self.needsInitialDraw = False
		self.dirty = 1
		newX = self.rect[0] + 2**ZOOM_LVL * self.xVel
		newY = self.rect[1] + 2**ZOOM_LVL * self.yVel
		self.rect = (newX, newY, self.rect[2], self.rect[3])
		# Update old (previous frame) velocities
		self.oldXVel = self.xVel
		self.oldYVel = self.yVel
		self.xVel = self.yVel = 0
		
		# Hard coded animation for player
		# self.frame * 16 is probably unreadable and stupid
		if self.dir == Protagonist.NORTH:
			self.area = rectZoom((16, self.frame * 16, 16, 16))
		elif self.dir == Protagonist.SOUTH:
			self.area = rectZoom((0,self.frame * 16, 16, 16))
		elif self.dir == Protagonist.EAST:
			self.area = rectZoom((32,self.frame * 16, 16, 16))
		elif self.dir == Protagonist.WEST:
			self.area = rectZoom((48,self.frame * 16, 16, 16))
		
		# Update frame #
		if self.frameChangeCount < Protagonist.FRAMES_PER_STILL:
			self.frameChangeCount += 1
		else:
			self.frameChangeCount = 0
			if self.frame == 1: self.frame = 0
			else: self.frame = 1
# Tile class: super class for objects sharing the simple_tileset.png file
class Tile(IcySprite):
	def __init__(self, rect, sheet, area = (0,0,0,0)):
		IcySprite.__init__(self, rect, sheet, area)
	def update(self):
		pass
		
class GroundTile(Tile):
	def __init__(self, rect, sheet, area = (0,0,16,16)):
		Tile.__init__(self, rect, sheet, area)
	
class BlockTile(Tile):
	def __init__(self, rect, sheet, area = (48,0,16,16)):
		Tile.__init__(self, rect, sheet, area)

class KeyDoorTile(Tile):
	def __init__(self, rect, sheet, area = (32,0,16,16)):
		Tile.__init__(self, rect, sheet, area) 

class SpecialTile(Tile):
	def __init__(self, rect, sheet, area = (0,48,16,16)):
		Tile.__init__(self, rect, sheet, area) 
