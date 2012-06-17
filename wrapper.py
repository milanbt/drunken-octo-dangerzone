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
		
		# Tuple of all game objects
		self.sprites = (\
			Protagonist((0,0,16,16), EARL_SHEET),\
			GrassTile((0,0,16,16), TILE_SHEET),\
			GrassTile((16,0,16,16), TILE_SHEET),\
			GrassTile((32,0,16,16), TILE_SHEET),\
			GrassTile((48,0,16,16), TILE_SHEET),\
			GrassTile((0,16,16,16), TILE_SHEET),\
			GrassTile((16,16,16,16), TILE_SHEET),\
			GrassTile((32,16,16,16), TILE_SHEET),\
			GrassTile((48,16,16,16), TILE_SHEET),\
			GrassTile((0,0,16,16), TILE_SHEET),\
			GrassTile((16,0,16,16), TILE_SHEET),\
			GrassTile((32,0,16,16), TILE_SHEET),\
			GrassTile((48,0,16,16), TILE_SHEET),\
			GrassTile((0,16,16,16), TILE_SHEET),\
			GrassTile((16,16,16,16), TILE_SHEET),\
			GrassTile((32,16,16,16), TILE_SHEET),\
			GrassTile((48,16,16,16), TILE_SHEET))
	# Calls update on every sprite
	def update(self):
		for s in self.sprites:
			# Efficiency could be improved for dirtyRects
			oldRect = s.rect
			s.update()
			if s.dirty == 1:
				self.dirtyRects.append(s.rect)
				self.dirtyRects.append(oldRect)
	# Draws all game sprites
	def draw(self):
		for r in self.dirtyRects:
			self.screen.fill((0,0,0), r)
		for s in self.sprites:
			s.draw(self.screen)
	def flip(self):
		pygame.display.update(self.dirtyRects)
		self.dirtyRects = []
		