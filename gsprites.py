import pygame, utils

# Player character class
class Protagonist(pygame.sprite.DirtySprite):
	def __init__(self, imgPath, rect):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = utils.loadImage(imgPath)
		self.rect = rect
		self.xVel, self.yVel = 0, 0
		self.health = 100
	def update(self):
		if self.xVel == 0 and self.yVel == 0:
			self.dirty = 0
			return
		self.dirty = 1
		newX = self.rect[0] + self.xVel
		newY = self.rect[1] + self.yVel
		self.rect = (newX, newY, self.rect[2], self.rect[3])
		self.xVel = self.yVel = 0
	def draw(self, surface):
		if self.dirty == 1:
			surface.blit(self.image, self.rect)

# Enemy class
class Enemy(pygame.sprite.DirtySprite):
	def __init__(self, imgPath, rect):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = utils.loadImage(imgPath)
		self.rect = rect
		self.xVel, self.yVel = 0, 0
		self.health = 100
	def update(self):
		newX = self.rect[0] + self.xVel
		newY = self.rect[1] + self.yVel
		self.rect = (newX, newY, self.rect[2], self.rect[3])
		self.xVel = self.yVel = 0
		
# Brick obstacle class
class Brick(pygame.sprite.DirtySprite):
	def __init__(self, imgPath, rect):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = utils.loadImage(imgPath)
		self.rect = rect
	def update(self):
		pass
