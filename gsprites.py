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
		self.latestKeyPresses = []
		# | Fixes bug where character isn't drawn when game starts
		# V until the user presses an arrow key
		self.needsInitialDraw = True
	def update(self):
	
		if len(self.latestKeyPresses) != 0:
			if self.latestKeyPresses[0] == K_UP:
				self.dir = Protagonist.NORTH
			elif self.latestKeyPresses[0] == K_DOWN:
				self.dir = Protagonist.SOUTH
			elif self.latestKeyPresses[0] == K_LEFT:
				self.dir = Protagonist.WEST
			elif self.latestKeyPresses[0] == K_RIGHT:
				self.dir = Protagonist.EAST
		keyPressed = pygame.key.get_pressed()
		if self.dir == Protagonist.NORTH and keyPressed[K_UP]:
			self.yVel -= 4
		if self.dir == Protagonist.SOUTH and keyPressed[K_DOWN]: 
			self.yVel += 4
		if self.dir == Protagonist.EAST and keyPressed[K_RIGHT]: 
			self.xVel += 4
		if self.dir == Protagonist.WEST and keyPressed[K_LEFT]:
			self.xVel -= 4
		if (not self.needsInitialDraw) and self.xVel == 0 and self.yVel == 0:
			self.dirty = 0
			return
		if self.needsInitialDraw:
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

# Constants for the lake part locations on the scaled sprite sheet
TL_ = rectZoom((16,16,16,16))
T_ = rectZoom((32,16,16,16))
TR_ = rectZoom((48,16,16,16))
R_ = rectZoom((48,32,16,16))
BR_ = rectZoom((48,48,16,16))
B_ = rectZoom((32,48,16,16))
BL_ = rectZoom((16,48,16,16))
L_ = rectZoom((16,32,16,16))
M_ = rectZoom((32,32,16,16))
class LakeSprite(Tile):
	def __init__(self, rect, sheet, area = (0,0,0,0)):
		Tile.__init__(self, rect, sheet, area)
		self.rect = rect
	def draw(self, surface):
		if self.dirty == 1:
			for i in range(int(self.rect[2]/16)):
				for j in range(int(self.rect[3]/16)):
					if i == 0 and j == 0:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							TL_)
					elif i == 0 and j == self.rect[3]/16 - 1:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							BL_)
					elif j == 0 and i == self.rect[2]/16 - 1:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							TR_)
					elif i == self.rect[2]/16 - 1 and \
						j == self.rect[3]/16 - 1:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							BR_)
					elif i == 0:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							L_)
					elif i == self.rect[2]/16 - 1:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							R_)
					elif j == 0:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							T_)
					elif j == self.rect[3]/16 - 1:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							B_)
					else:
						surface.blit(self.sheet,\
							((self.rect[0]+i*16) * 2**ZOOM_LVL,\
								(self.rect[1]+j*16) * 2**ZOOM_LVL,
								16 * 2**ZOOM_LVL,\
								16 * 2**ZOOM_LVL),\
							M_)
			self.dirty = 0
class KeyDoorTile(Tile):
	def __init__(self, rect, sheet, area = (32,0,16,16)):
		Tile.__init__(self, rect, sheet, area) 

class SpecialTile(Tile):
	def __init__(self, rect, sheet, area = (0,48,16,16)):
		Tile.__init__(self, rect, sheet, area) 
