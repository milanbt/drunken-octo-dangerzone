import pygame, utils

# Should look at pygame docs and examples of 
# sprite sheet use with built in sprite classes.
# Current implementation could probably do without
# inheriting from DirtySprite

# Player character class
class Protagonist(pygame.sprite.DirtySprite):
	def __init__(self, rect):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = utils.loadImage('gfx/earl_of_ice.png')
		self.currentFrameRect = (0,0,16,16)
		self.rect = rect
		self.xVel, self.yVel = 0, 0
		self.health = 100
	def update(self):
		if self.xVel == 0 and self.yVel == 0:
			self.dirty = 0
			return
		self.dirty = 1
		newX = self.rect[0] + self.xVel
		newY = self.rect[1] + self.yVel
		self.rect = (newX, newY, self.rect[2], self.rect[3])
		self.xVel = self.yVel = 0
	def draw(self, surface):
		if self.dirty == 1:
			surface.blit(self.image, self.rect, self.currentFrameRect)

	
# Tile class: super class for objects sharing the simple_tileset.png file
class Tile(pygame.sprite.DirtySprite):
	img = None
	def __init__(self, rect):
		pygame.sprite.DirtySprite.__init__(self)		
		self.rect = rect
		img = utils.loadImage('gfx/simple_tileset.png')
	def update(self):
		pass

class GrassTile(Tile):
	def __init__(self, rect):
		Tile.__init__(self, rect)
		self.sheetArea = (0,0,16,16)
		
class RoadTile(Tile):
	def __init__(self, rect):
		Tile.__init__(self, rect)
		self.sheetArea = (16,0,16,16)
	
class BlockTile(Tile):
	def __init__(self, rect):
		Tile.__init__(self, rect)
		self.sheetArea = (48,0,16,16)
		
def drawTiles(tiles, surface):
	for t in tiles:
		surface.blit(t.img, t.rect, t.sheetArea)
	
		
''' Not yet necessary --------------------

# Enemy class
class Enemy(pygame.sprite.DirtySprite):
	def __init__(self, imgPath, rect):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = utils.loadImage(imgPath)
		self.rect = rect
		self.xVel, self.yVel = 0, 0
		self.health = 100
	def update(self):
		newX = self.rect[0] + self.xVel
		newY = self.rect[1] + self.yVel
		self.rect = (newX, newY, self.rect[2], self.rect[3])
		self.xVel = self.yVel = 0
------------------------------------------ '''	