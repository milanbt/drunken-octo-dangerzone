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
while(not stage.exit):
	
	stage.update()
	stage.draw()
	stage.flip()
	
	# Manage frame rate
	clock.tick(24)
	
	# Should show fps on screen using clock.get_fps()
	