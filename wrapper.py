import pygame
from pygame.locals import *
from gsprites import *

# Helper function for image loading
def loadImage(filePath):
	ret = pygame.Surface.convert_alpha(pygame.image.load(filePath))
	for i in range(ZOOM_LVL):
		ret = pygame.transform.scale(ret, \
			(ret.get_width()*2, ret.get_height()*2))
	return ret

# Stage class to hold, update, and draw sprites
class Stage:
	EARL_SHEET = None
	TILE_SHEET = None
	def __init__(self, screenSize):
		# Initialize pygame and display module
		pygame.init()
		pygame.display.init()
		
		# List of rectangles that defines the areas 
		# that need to be pygame.display.update'd
		self.dirtyRects = []
		
		# When set true, game exits
		self.exit = False
		
		# Create screen to draw on
		self.screen = pygame.display.set_mode(screenSize)
		
		# Class constants holding the sprite sheet surfaces
		EARL_SHEET = loadImage('gfx/earl_of_ice.png')
		TILE_SHEET = loadImage('gfx/simple_tileset.png')
		GRASS_AREA = (0,0,16,16)
		ROAD_AREA = (16,0,16,16)
		TREE_AREA = (0,16,16,32)
		SPECIAL_AREA = (0,48,16,16)
		BLOCK_AREA = (48,0,16,16)
		KEYDOOR_AREA = (32,0,16,16)
		# All game objects
		self.earl = Protagonist((0,0,16,16), EARL_SHEET);
		self.floorTiles = (\
			GroundTile((0,0,16,16), TILE_SHEET, GRASS_AREA),\
			GroundTile((16,0,16,16), TILE_SHEET, GRASS_AREA),\
			GroundTile((32,0,16,16), TILE_SHEET, ROAD_AREA),\
			GroundTile((48,0,16,16), TILE_SHEET, GRASS_AREA),\
			GroundTile((0,16,16,16), TILE_SHEET, GRASS_AREA),\
			GroundTile((16,16,16,16), TILE_SHEET, GRASS_AREA),\
			GroundTile((32,16,16,16), TILE_SHEET, ROAD_AREA),\
			GroundTile((48,16,16,16), TILE_SHEET, GRASS_AREA),\
			)
		self.blockTiles = (\
			BlockTile((32,16,16,16), TILE_SHEET, BLOCK_AREA),\
			BlockTile((48,16,16,16), TILE_SHEET, BLOCK_AREA),\
			BlockTile((32,32,16,32), TILE_SHEET, TREE_AREA))
					
		self.specialTiles = (\
			SpecialTile((0,16,16,16), TILE_SHEET),)
		self.keyDoorTiles = (\
			KeyDoorTile((16,16,16,16), TILE_SHEET),)
		self.lakeSprites = (\
			LakeSprite((0,64,48,48), TILE_SHEET),\
			LakeSprite((128,64,32,64), TILE_SHEET),\
			LakeSprite((0,256,80,32), TILE_SHEET))
	# Calls update on every sprite
	def update(self):
		# Event loop that checks for exit conditions and
		# keyboard input
		for event in pygame.event.get():
			if event.type == QUIT:
				self.exit = True
				break
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.exit = True
					break
				self.earl.latestKeyPresses.insert(0, event.key)
				print event.key
			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					self.exit = True
					break
				self.earl.latestKeyPresses.remove(event.key)
		# Something said to do this; should work without it
		pygame.event.pump()
		
		oldRect = self.earl.rect
		self.earl.update()
		if self.earl.dirty == 1:
			self.dirtyRects.append(self.earl.rect)
			self.dirtyRects.append(oldRect)
		for bt in self.blockTiles:
			if pygame.Rect(self.earl.rect).colliderect(bt.rect):
				self.dirtyRects.remove(self.earl.rect)
				self.earl.rect = (\
					self.earl.rect[0] - 2**ZOOM_LVL * self.earl.oldXVel,\
					self.earl.rect[1] - 2**ZOOM_LVL * self.earl.oldYVel,\
					self.earl.rect[2], self.earl.rect[3])
			bt.update()
			if bt.dirty == 1:
				self.dirtyRects.append(bt.rect)
		for st in self.specialTiles:
			if pygame.Rect(self.earl.rect).colliderect(st.rect):
				self.dirtyRects.remove(self.earl.rect)
				self.earl.rect = (\
					self.earl.rect[0] - 2**ZOOM_LVL * self.earl.oldXVel,\
					self.earl.rect[1] - 2**ZOOM_LVL * self.earl.oldYVel,\
					self.earl.rect[2], self.earl.rect[3])
			st.update()
			if st.dirty == 1:
				self.dirtyRects.append(st.rect)
		for kdt in self.keyDoorTiles:
			if pygame.Rect(self.earl.rect).colliderect(kdt.rect):
				self.dirtyRects.remove(self.earl.rect)
				self.earl.rect = (\
					self.earl.rect[0] - 2**ZOOM_LVL * self.earl.oldXVel,\
					self.earl.rect[1] - 2**ZOOM_LVL * self.earl.oldYVel,\
					self.earl.rect[2], self.earl.rect[3])
			kdt.update()
			if kdt.dirty == 1:
				self.dirtyRects.append(kdt.rect)
		for st in self.lakeSprites:
			if pygame.Rect(self.earl.rect).colliderect(rectZoom(st.rect)):
				self.dirtyRects.remove(self.earl.rect)
				self.earl.rect = (\
					self.earl.rect[0] - 2**ZOOM_LVL * self.earl.oldXVel,\
					self.earl.rect[1] - 2**ZOOM_LVL * self.earl.oldYVel,\
					self.earl.rect[2], self.earl.rect[3])
			st.update()
			if st.dirty == 1:
				self.dirtyRects.append(rectZoom(st.rect))
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
		for st in self.specialTiles:
			st.draw(self.screen)
		for kdt in self.keyDoorTiles:
			kdt.draw(self.screen)
		for ls in self.lakeSprites:
			ls.draw(self.screen)
		self.earl.draw(self.screen)
	def flip(self):
		pygame.display.update(self.dirtyRects)
		self.dirtyRects = []
		