import pygame

# Image loading function
def loadImage(filePath):
	return pygame.Surface.convert_alpha(pygame.image.load(filePath))
