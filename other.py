# Connecting libraries
import pygame

# Connecting files
from settings import *
from storage import *

# Load image
def loadImage(src):
	image = pygame.image.load(src)
	return image

# Rendering load image
def drawImage(screen, image, xy):
	screen.blit(image, xy)

# Unscalable image
def unImage(screen, src, xy):
	image = pygame.image.load(src)
	screen.blit(image, xy)

# Scalable image
def scImage(screen, src, xy, size):
	image = pygame.image.load(src)
	image = pygame.transform.scale(image, size)
	screen.blit(image, xy)

def gridSize(xy):
	x = int(xy[0] / GRIDLINEX) * GRIDLINEX
	y = int(xy[1] / GRIDLINEX) * GRIDLINEX
	return (x, y)

def drawGrid(screen):
	collsX = WIDTH / GRIDLINEX
	collsY = HEIGHT / GRIDLINEY
	condition = (GRIDLINEX * collsX, GRIDLINEY * collsY)
	for i in range(int(condition[0])):
		if i % GRIDLINEX == 0:
			pygame.draw.line(screen, GRIDCOLOR, (i, 0), (i, HEIGHT))
	for i in range(int(condition[1])):
		if i % GRIDLINEY == 0:
			pygame.draw.line(screen, GRIDCOLOR, (0, i), (WIDTH, i))
