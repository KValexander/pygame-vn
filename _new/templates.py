# Connection libraries
import pygame
import os

# Connecting files
from settings import *
from common import *

# Classes:
#	Icon
# 	Link
# 	Text
# 	Surface
# 	Inscription


# class Icon
class Icon:
	def __init__(self, name, src, xy, wh, folder):
		# Custom variables
		self.name 	= name
		self.src  	= src
		self.xy   	= xy
		self.wh   	= wh
		self.folder = folder

		# Boolean variables
		self.hide 		= False
		self.hover 		= False
		self.selected 	= False

		# Default variables
		self.pathToImage = self.folder + self.src
		if self.wh != None: self.image = scLoadImage(self.pathToImage, self.wh)
		else: self.image = loadImage(self.pathToImage)
		self.rect = self.image.get_rect()

	# Rendering icon
	def draw(self, window):
		window.blit(self.image, self.xy)

# class Link
class Link:
	def __init__(self, name, value, xy, color, aim, selected, size, font):
		# Custom variables
		self.name 			= name
		self.value 			= str(value)
		self.xy 			= xy
		self.color 			= color
		self.coloraim 		= aim
		self.colorselected  = selected
		self.size 			= size
		self.font 			= pygame.font.SysFont(font, self.size)

		# Boolean variables
		self.hide 		= False
		self.hover 		= False
		self.selected 	= False

		# Default variables
		self.twh 			= self.font.size(self.value)
		self.iname 			= self.font.render(self.value, True, self.color)
		self.rect 			= self.iname.get_rect()

	# Rendering link
	def draw(self, window):
		if self.hover:
			self.iname = self.font.render(self.value, True, self.coloraim)
		else: self.iname = self.font.render(self.value, True, self.color)
		
		if self.selected:
			self.iname = self.font.render(self.value, True, self.colorselected)

		window.blit(self.iname, self.xy)

	# Select link
	def select(self):
		self.selected = True

# class Text
class Text:
	def __init__(self, name, value, xy, width, color, size, lh, font):
		# Custom variables
		self.name 	= name
		self.value 	= str(value)
		self.xy 	= xy
		self.width 	= width
		self.color 	= color
		self.size 	= size
		self.lh 	= lh
		self.font 	= pygame.font.SysFont(font, self.size)
		self.y 		= xy[1]

		# Boolean variables
		self.hide = False

		# Default variables
		self.outLines = []
		self.iline = ""
		self.lines = processingLine(self.value, self.width, self.font)

		# Set out lines
		self.setOutLines()

	# Set out lines
	def setOutLines(self):
		self.outLines.clear()
		for value in self.lines:
			self.iline = self.font.render(str(value), True, self.color)
			self.outLines.append(self.iline)

	# Rendering text
	def draw(self, window):
		self.y = self.xy[1]
		for line in self.outLines:
			window.blit(line, (self.xy[0], self.y))
			self.y += self.lh

# class Link
class Surface:
	def __init__(self, name, alpha, color, xy, wh):
		# Custom variables
		self.name = name
		self.alpha = alpha
		self.color = color
		self.xy = xy
		self.wh = wh

		# Boolean variables
		self.hide = False

		# Default variables
		self.surface = pygame.Surface(self.wh)
		self.surface.fill(self.color)
		self.surface.set_alpha(self.alpha)

	# Surface rendering
	def draw(self, window):
		if self.hide == False:
			window.blit(self.surface, self.xy)

# class Link
class Inscription:
	def __init__(self, name, value, xy, color, size, font):
		# Custom variables
		self.name 	= name
		self.value 	= value
		self.color 	= color
		self.size 	= size
		self.xy 	= xy

		# Defaults variables
		self.font 	= pygame.font.SysFont(font, self.size)
		self.twh 	= self.font.size(self.value)
		self.iname 	= self.font.render(str(self.value), True, self.color)
		self.rect 	= self.iname.get_rect()

	# Inscription rendering
	def draw(self, window):
		window.blit(self.iname, self.xy)