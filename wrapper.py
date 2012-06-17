import pygame
from pygame.locals import *
import utils
from gsprites import *

# Helper function for image loading
def loadImage(filePath):
	return pygame.Surface.convert_alpha(pygame.image.load(filePath))

# Stage class to hold, update, and draw sprites
class Stage:
	EARL_SHEET = None
	TILE_SHEET = None
	def __init__(self):
		# Initialize pygame and display module
		pygame.init()
		pygame.display.init()
		
		# List of rectangles that defines the areas 
		# that need to be pygame.display.update'd
		self.dirtyRects = []
		
		# Create screen to draw on
		self.screen = pygame.display.set_mode((480,272))
		
		# Class constants holding the sprite sheet surfaces
		EARL_SHEET = utils.loadImage('gfx/earl_of_ice.png')
		TILE_SHEET = utils.loadImage('gfx/simple_tileset.png')
		
		# All game objects
		self.earl = Protagonist((0,0,16,16), EARL_SHEET);
		self.floorTiles = (\
			GrassTile((0,0,16,16), TILE_SHEET),\
			GrassTile((16,0,16,16), TILE_SHEET),\
			RoadTile((32,0,16,16), TILE_SHEET),\
			GrassTile((48,0,16,16), TILE_SHEET),\
			GrassTile((0,16,16,16), TILE_SHEET),\
			GrassTile((16,16,16,16), TILE_SHEET),\
			RoadTile((32,16,16,16), TILE_SHEET),\
			GrassTile((48,16,16,16), TILE_SHEET),\
			)
		self.blockTiles = (\
			BlockTile((32,16,16,16), TILE_SHEET),\
			BlockTile((48,16,16,16), TILE_SHEET))
	# Calls update on every sprite
	def update(self):
		oldRect = self.earl.rect
		self.earl.update()
		if self.earl.dirty == 1:
			self.dirtyRects.append(self.earl.rect)
			self.dirtyRects.append(oldRect)
		for bt in self.blockTiles:
			if pygame.Rect(self.earl.rect).colliderect(bt.rect):
				self.dirtyRects.remove(self.earl.rect)
				self.earl.rect = (\
					self.earl.rect[0] - self.earl.oldXVel,\
					self.earl.rect[1] - self.earl.oldYVel,\
					self.earl.rect[2], self.earl.rect[3])
		for ft in self.floorTiles:
			if pygame.sprite.collide_rect(ft, self.earl) or\
				pygame.Rect(oldRect).colliderect(ft.rect):
				if self.earl.dirty == 1:
					ft.dirty = 1
			ft.update()
			if ft.dirty == 1:
				self.dirtyRects.append(ft.rect)
	# Draws all game sprites
	def draw(self):
		for r in self.dirtyRects:
			self.screen.fill((0,0,0), r)
		for ft in self.floorTiles:
			ft.draw(self.screen)
		for bt in self.blockTiles:
			bt.draw(self.screen)
		self.earl.draw(self.screen)
	def flip(self):
		pygame.display.update(self.dirtyRects)
		self.dirtyRects = []
		