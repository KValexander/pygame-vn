# Connecting libraries
import pygame

# Connecting file
from settings import *

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
def defineCoord(coord, wh):
	coord = coord.replace(" ", "")
	coord = removeChar(coord).split(",")
	if float(coord[0]) == 0.0: x = 0
	else: x = wh[0] * float(coord[0])
	if float(coord[1]) == 0.0: y = 0
	else: y = wh[1] * float(coord[1])
	coord = (x, y)
	return coord

# Define resolution
def defineResolution(size):
	size = size.replace(" ", "")
	size = removeChar(size).split(",")
	size = (int(size[0]), int(size[1]))
	return size


# check for common commands
def commonCommands(line):
	command = line.split(" ")[0]
	if command == "#": return False
	elif command == "//": return False
	elif command[0] == "#": return False
	elif command[0] == "//": return False
