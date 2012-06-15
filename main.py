import os
import pygame
from pygame.locals import *
import utils, gsprites

# Initialize pygame and display module
pygame.init()
pygame.display.init()

# Create empty dirtyRects list of rectangles for efficient drawing
dirtyRects = []

# Create screen to draw on
screen = pygame.display.set_mode((480,272))

art = gsprites.Protagonist('articuno.gif', (0,0,32,32))
brick1 = gsprites.Brick('brick.png', (32,0,32,32))
brick2 = gsprites.Brick('brick.png', (32,32,32,32))
brick3 = gsprites.Brick('brick.png', (0,32,32,32))

bricks = pygame.sprite.Group(brick1, brick2, brick3)

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
	if keyPressed[K_UP]: art.yVel -= 4
	if keyPressed[K_DOWN]: art.yVel += 4
	if keyPressed[K_RIGHT]: art.xVel += 4
	if keyPressed[K_LEFT]: art.xVel -= 4
	
	# Fills a black default background in places where things moved	
	if art.dirty == 1:	
		screen.fill((0, 0, 0), art.rect)
	
	# dirtyRects: collection of rects where screen has changed
	dirtyRects.append(art.rect)
	
	# gsprites.Protagonist's update sets all it's velocities to 0 after 
	# incrementing its position with them
	art.update()
	
	dirtyRects.append(art.rect)
	for b in bricks.sprites():
		dirtyRects.append(b.rect)
	
	# All drawing here
	art.draw(screen)
	bricks.draw(screen)
	
	# Redraw dirty parts of screen
	pygame.display.update(dirtyRects)
	
	# Something said to do this; should work without it
	pygame.event.pump()
	
	# Manage frame rate
	clock.tick(24)
	
	# Should show fps on screen using clock.get_fps()
	
	