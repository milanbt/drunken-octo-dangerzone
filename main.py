import os
import pygame
from pygame.locals import *
import utils, gsprites


# Initialize pygame and display module
pygame.init()
pygame.display.init()

# Create screen to draw on
screen = pygame.display.set_mode((1024,768))

art = gsprites.Protagonist('articuno.gif', (0,0,0,0))
brick1 = gsprites.Brick('brick.png', (32,0,0,0))
brick2 = gsprites.Brick('brick.png', (32,32,0,0))
brick3 = gsprites.Brick('brick.png', (0,32,0,0))

bricks = pygame.sprite.Group(brick1, brick2, brick3)

exit = False
clock = pygame.time.Clock()

# Main game loop
while(not exit):
	# Event loop that checks for exit conditions
	for event in pygame.event.get():
		if event.type == QUIT:
			exit = True
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			exit = True
		''' Old code that doesn't work correctly
		elif event.type == KEYDOWN and event.key == K_UP:
			art.yVel = -1
		elif event.type == KEYDOWN and event.key == K_DOWN:
			art.yVel = 1
		elif event.type == KEYDOWN and event.key == K_LEFT:
			art.xVel = -1
		elif event.type == KEYDOWN and event.key == K_RIGHT:
			art.xVel = 1
		elif event.type == KEYUP and event.key == K_UP:
			if not keyPressed[pygame.K_DOWN]:
				art.yVel = 0
			else: art.yVel = 1
		elif event.type == KEYUP and event.key == K_DOWN:
			if not keyPressed[pygame.K_UP]:
				art.yVel = 0
			else: art.yVel = -1
		elif event.type == KEYUP and event.key == K_LEFT:
			if not keyPressed[pygame.K_RIGHT]:
				art.xVel = 0
			else: art.xVel = 1
		elif event.type == KEYUP and event.key == K_RIGHT:
			if not keyPressed[pygame.K_LEFT]:
				art.xVel = 0
			else: art.xVel = -1
		'''
	
	# Key states for player movement
	keyPressed = pygame.key.get_pressed()
	if keyPressed[pygame.K_UP]: art.yVel -= 4
	if keyPressed[pygame.K_DOWN]: art.yVel += 4
	if keyPressed[pygame.K_RIGHT]: art.xVel += 4
	if keyPressed[pygame.K_LEFT]: art.xVel -= 4
	
	# Fills a black default background			
	screen.fill(0x000000)
	
	# gsprites.Protagonist's update sets all it's velocities to 0 after 
	# incrementing its position with them
	art.update()
	
	# All drawing here
	art.draw(screen)
	bricks.draw(screen)
	
	# Redraw the screen
	pygame.display.flip()
	
	# Manage frame rate
	clock.tick(60)
	
	