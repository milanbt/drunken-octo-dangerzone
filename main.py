import pygame
from pygame.locals import *
import wrapper
from gsprites import *

exit = False
clock = pygame.time.Clock()

stage = wrapper.Stage((800,600))
	
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
	
	stage.update()
	stage.draw()
	stage.flip()
	# Something said to do this; should work without it
	pygame.event.pump()
	
	# Manage frame rate
	clock.tick(24)
	
	# Should show fps on screen using clock.get_fps()
	