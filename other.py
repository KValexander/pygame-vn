import pygame

from settings import *
from storage import *

def loadImage(src):
	image = pygame.image.load(src)
	return image

def drawImage(screen, image, rect):
	screen.blit(image, rect)

def univImage(screen, src, rect):
	image = pygame.image.load(src)
	screen.blit(image, rect)

def gridSize(number, case):
	if case == "x":
		number = int(n / GRIDLINEX) * GRIDLINEX
	elif case == "y":
		number = int(n / GRIDLINEY) * GRIDLINEY
	else:
		number = int(n / GRIDLINEX) * GRIDLINEX
	return number

def drawGrid(screen):
	collsX = WIDTH / GRIDLINEX
	collsY = HEIGHT / GRIDLINEY
	condition = (GRIDLINEX * collsX, GRIDLINEY * collsY)
	for i in range(int(condition[0])):
		if i % GRIDLINEX == 0:
			pygame.draw.line(screen, WHITE, (i, 0), (i, HEIGHT))
	for i in range(int(condition[1])):
		if i % GRIDLINEY == 0:
			pygame.draw.line(screen, WHITE, (0, i), (WIDTH, i))
