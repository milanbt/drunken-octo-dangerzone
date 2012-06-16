import pygame
from pygame.locals import *
import utils
from gsprites import *

# Initialize pygame and display module
pygame.init()
pygame.display.init()

# Create empty dirtyRects list of rectangles for efficient drawing
dirtyRects = []

# Create screen to draw on
screen = pygame.display.set_mode((480,272))

# Create map editor at some point
earl = Protagonist((0,0,16,16))
grassTiles = [\
	GrassTile((0,0,16,16)),\
	GrassTile((16,0,16,16)),\
	GrassTile((32,0,16,16)),\
	GrassTile((48,0,16,16)),\
	GrassTile((0,16,16,16)),\
	GrassTile((16,16,16,16)),\
	GrassTile((32,16,16,16)),\
	GrassTile((48,16,16,16))]
roadTiles = [\
	RoadTile((64,0,16,16)),\
	RoadTile((64,16,16,16))]

exit = False
clock = pygame.time.Clock()

##################
# MAIN GAME LOOP #
##################
while(not exit):
	# Event loop that checks for exit conditions
	for event in pygame.event.get():
		if event.type == QUIT:
			exit = True
			break
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			exit = True
			break

	# Key states for player movement
	keyPressed = pygame.key.get_pressed()
	if keyPressed[K_UP]: 
		earl.yVel -= 4
		earl.xVel = 0
	if keyPressed[K_DOWN]: 
		earl.yVel += 4
		earl.xVel = 0
	if keyPressed[K_RIGHT]: 
		earl.xVel += 4
		earl.yVel = 0
	if keyPressed[K_LEFT]: 
		earl.xVel -= 4
		earl.yVel = 0
	
	# Fills a black default background in places where things moved	
	if earl.dirty == 1:	
		screen.fill((0, 0, 0), earl.rect)
	
	# dirtyRects: collection of rects where screen has changed
	dirtyRects.append(earl.rect)
	
	# gsprites.Protagonist's update sets all it's velocities to 0 after 
	# incrementing its position with them
	earl.update()
	
	dirtyRects.append(earl.rect)
	
	# dirtyRects still needs to account for tiles being walked on and such
	
	# All drawing here
	drawTiles(grassTiles, screen)
	drawTiles(roadTiles, screen)
	earl.draw(screen)
	
	# Redraw dirty pearls of screen
	pygame.display.update(dirtyRects)
	
	# Something said to do this; should work without it
	pygame.event.pump()
	
	# Manage frame rate
	clock.tick(24)
	
	# Should show fps on screen using clock.get_fps()
	
	