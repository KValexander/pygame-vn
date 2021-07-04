# Connecting libraries
import pygame

# Connecting files
from settings import *
from storage import *
from other import *

# Button class
class Button:
	def __init__(self, name, value, tcolor, xy, wh, bcolor):
		# Custom variables
		self.name 	= name
		self.value 	= value
		self.tcolor = tcolor
		self.xy 	= xy
		self.wh 	= wh
		self.bcolor = bcolor

		# Somewhere in between the world
		self.xywh 	= (self.xy, self.wh)

		# Boolean variables
		self.click 	= False
		self.hover 	= False

		# Defaults variables
		self.font 	= pygame.font.SysFont("calibri", 20)
		self.twh 	= self.font.size(self.value)
		self.loc 	= (self.xy[0] + self.wh[0] / 2 - self.twh[0] / 2, self.xy[1] + self.wh[1] / 2 - self.twh[1] / 2)
		self.rect	= pygame.Rect(self.xywh)
		self.iname	= self.font.render(str(self.value), True, self.tcolor)

	# Button rendering
	def draw(self, screen):
		pygame.draw.rect(screen, self.bcolor, self.rect, 0)
		screen.blit(self.iname, self.loc)

		if self.hover == True:
			pygame.draw.rect(screen, BLACK, self.rect, 3)

# Surface class
class Surface:
	def __init__(self, name, color, alpha, xy, wh):
		# Custom variables
		self.name = name
		self.color = color
		self.alpha = alpha
		self.xy = xy
		self.wh = wh

		# Default variables
		self.hide = False
		self.surface = pygame.Surface(self.wh)
		self.surface.fill(self.color)
		self.surface.set_alpha(self.alpha)

	# Surface rendering
	def draw(self, screen):
		if self.hide == False:
			screen.blit(self.surface, self.xy)

# Inscription class
class Inscription:
	def __init__(self, name, value, color, xy, size):
		# Custom variables
		self.name 	= name
		self.value 	= value
		self.color 	= color
		self.size 	= size
		self.xy 	= xy

		# Defaults variables
		self.font 	= pygame.font.SysFont("calibri", self.size)
		self.twh 	= self.font.size(self.value)
		self.loc 	= (self.xy[0] - self.twh[0] / 2, self.xy[1] - self.twh[1] / 2)
		self.iname 	= self.font.render(str(self.value), True, self.color)
		self.rect 	= self.iname.get_rect()

	# Inscription rendering
	def draw(self, screen):
		screen.blit(self.iname, self.xy)

# Link class
class Link:
	def __init__(self):
		pass

# Texture class
class Texture:
	def __init__(self):
		pass

# Cell load/save class
class Cell:
	def __init__(self):
		pass