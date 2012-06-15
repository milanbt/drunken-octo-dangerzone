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

art = gsprites.Protagonist('articuno.gif', (0.0,0.0,32.0,32.0))
brick1 = gsprites.Brick('brick.png', (32,0,32,32))
brick2 = gsprites.Brick('brick.png', (32,32,32,32))
brick3 = gsprites.Brick('brick.png', (0,32,32,32))

bricks = pygame.sprite.Group(brick1, brick2, brick3)

exit = False
clock = pygame.time.Clock()

# Main game loop
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
	
	# Fills a black default background			
	screen.fill((0, 0, 0))
	
	# dirtyRects: collection of rects where screen has changed
	dirtyRects = [art.rect]
	
	# gsprites.Protagonist's update sets all it's velocities to 0 after 
	# incrementing its position with them
	art.update()
	
	
	dirtyRects.append(art.rect)
	for b in bricks.sprites():
		dirtyRects.append(b.rect)
	
	# All drawing here
	art.draw(screen)
	bricks.draw(screen)
	
	# Redraw the screen
	pygame.display.update(dirtyRects)
	
	# ???
	pygame.event.pump()
	
	# Manage frame rate
	clock.tick(24)
	
	# printed fps for debug purposes
	# *** Should be changed to blitting fps counter on screen ***
	# print clock.get_fps()
	
	