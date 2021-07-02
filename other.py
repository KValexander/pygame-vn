# Connecting libraries
import pygame

# Connecting files
from settings import *
from storage import *

# Handling mouse collision
def mouseCollision(xy, wh, pos):
	x, y = pos
	if( xy[0] < x and (xy[0] + wh[0]) > x
		and xy[1] < y and (xy[1] + wh[1] ) > y):
		return True
	else: return False

# Load image
def loadImage(src):
	image = pygame.image.load(src)
	return image

# Scalable load image
def scLoadImage(src, size):
	image = pygame.image.load(src)
	image = pygame.transform.scale(image, size)
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

# Removes the first and last characters
def removeChar(line):
	line = line[1 : -1]
	return line

# Cleaning variables from unnecessary text
def clearVariable(var, clear):
	var = var.replace(clear, "")
	var = var.replace(" ", "")
	var = var.split("=")
	return var

# To grid size
def gridSize(xy):
	x = int(xy[0] / GRIDLINEX) * GRIDLINEX
	y = int(xy[1] / GRIDLINEX) * GRIDLINEX
	return (x, y)

# Draw grid
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
