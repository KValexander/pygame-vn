# Connecting libraries
import pygame
import re

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

# Initial parsing of the line
def parsingLine(line):
	define = re.split(r"(^\w+)", line)
	define = [x for x in define if x != '']
	command, value = "", ""
	if len(define) >= 2:
		command, value = define[0], define[1]
	else: command = define[0]
	return command, value

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
	color = removeChar(color)
	arr = color.split(",")
	result = (int(arr[0]), int(arr[1]), int(arr[2]))
	return result

# Define size
def defineSize(size, wh):
	size = size.replace(" ", "")
	size = removeChar(size).split(",")
	if float(size[0]) == 0.0: x = 0
	else: x = wh[0] * float(size[0])
	if float(size[1]) == 0.0: y = 0
	else: y = wh[1] * float(size[1])
	size = (int(x), int(y))
	return size

# Fetch size
def fetchSize(size):
	size = size.replace(" ", "")
	size = removeChar(size).split(",")
	size = (int(abs(float(size[0]))), int(abs(float(size[1]))))
	return size

# Define one size
def defineOneSize(one, size):
	one = one.replace(" ", "")
	one = removeChar(one)
	one = size * float(one)
	return one

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

# Check screens
def getMainScreen(subscreen, config):
	screen = None
	for scr in config:
		if "subscreens" in config[scr]:
			if subscreen in config[scr]["subscreens"]:
				screen = scr
	return screen

# Retrieving an item by name
def getElementByName(name, arr):
	for element in arr:
		if name == element.name:
			return element
	return None

# Processing text on line
def processingLine(text, width, font):
	lines, words = [], text.split(" ")
	count, line = len(words), ""

	for i in range(count):
		textline = line + words[i] + " "
		textwh = font.size(textline)
		if textwh[0] > width:
			lines.append(line)
			line = words[i] + " "
		else: line = textline
		if i == count - 1: lines.append(line)

	return lines