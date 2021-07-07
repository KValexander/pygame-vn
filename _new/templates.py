# Connection libraries
import pygame
import os

# Connecting files
from settings import *
from common import *

# Classes:
# 	Link
# 	Surface
# 	Inscription

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