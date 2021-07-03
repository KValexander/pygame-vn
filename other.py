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

# Cleaning the lines
def clearLines(lines):
	badChars = ['\r', '\n', '\t']
	for i in range(len(lines)):
		for char in badChars:
			lines[i] = lines[i].replace(char, "")
	lines = [x for x in lines if x != '']
	return lines


# Define color
def defineColor(color):
	result = ()
	if color == "WHITE": result = WHITE
	elif color == "BLACK": result = BLACK
	else:
		color = removeChar(color)
		arr = color.split(",")
		result = (int(arr[0]), int(arr[1]), int(arr[2]))
	return result

# Define coordinates
def defineCoord(coord):
	coord = coord.replace(" ", "")
	coord = removeChar(coord).split(";")
	if float(coord[0]) == 0.0: x = 0
	else: x = WIDTH * float(coord[0])
	if float(coord[1]) == 0.0: y = 0
	else: y = HEIGHT * float(coord[1])
	coord = (x, y)
	return coord

# Define resolution
def defineResolution(size):
	size = size.replace(" ", "")
	size = removeChar(size).split(",")
	size = (int(size[0]), int(size[1]))
	return size
	# size = 

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
