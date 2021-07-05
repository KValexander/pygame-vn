# Connection libraries
import pygame
import os

# Connecting files
from settings import *
from common import *

# Classes:
# 	Link
#	Button
# 	Surfaces
# 	Inscription
#	Launcher

# Link class
class Link:
	def __init__(self, name, value, xy, rtrn):
		# Custom variables
		self.name 	= name
		self.value 	= value
		self.xy 	= xy
		self.rtrn 	= rtrn

		# Boolean variables
		self.hide 		= False
		self.hover 		= False
		self.selected 	= False

		# Default variables
		self.color 			= TEXTLINK
		self.coloraim 		= TEXTLINKAIM
		self.colorselected  = TEXTLINKSELECTED
		self.size 			= TEXTLINKSIZE
		self.sysfont 		= pygame.font.SysFont(TEXTSYSFONT, self.size)
		self.ownfont 		= pygame.font.Font(TEXTOWNFONT, self.size)
		self.twh 			= self.ownfont.size(self.value)
		self.iname 			= self.ownfont.render(self.value, True, self.color)
		self.rect 			= self.iname.get_rect()

	# Rendering link
	def draw(self, screen):
		screen.blit(self.iname, self.xy)

		if self.hover == True:
			self.iname = self.ownfont.render(self.value, True, self.coloraim)
		else:
			self.iname = self.ownfont.render(self.value, True, self.color)

	# Select link
	def select(self, screen):
		self.selected = True

# Button class
class Button:
	def __init__(self):
		pass

# Surface class
class Surface:
	def __init__(self, name, alpha, xy, wh):
		# Custom variables
		self.name 	= name
		self.alpha 	= alpha
		self.xy 	= xy
		self.wh 	= wh

		# Boolean variables
		self.hide = False

		# Default variables
		self.color 	 = SURFACE
		self.surface = pygame.Surface(self.wh)
		self.surface.fill(self.color)
		self.surface.set_alpha(self.alpha)
		self.rect 	 = self.surface.get_rect()

	# Rendering surface
	def draw(self, screen):
		screen.blit(self.surface, self.xy)

# Inscription class
class Inscription:
	def __init__(self, name, value, xy):
		# Custom variables
		self.name 	= name
		self.value	= str(value)
		self.xy 	= xy

		# BOoleand variables
		self.hide = False

		# Defaults variables
		self.color 	= TEXTINSCRIPTION
		self.size 	= TEXTINSCRIPTIONSIZE
		self.sysfont= pygame.font.SysFont(TEXTSYSFONT, self.size)
		self.ownfont= pygame.font.Font(TEXTOWNFONT, self.size)
		self.twh 	= self.ownfont.size(self.value)
		self.iname 	= self.ownfont.render(self.value, True, self.color)
		self.rect 	= self.iname.get_rect()

	# Rendering inscription
	def draw(self, screen):
		screen.blit(self.iname, self.xy)

# Launcher class
class Launcher:
	def __init__(self):
		# Launcher interface objects list
		self.links = []
		self.buttons = []
		self.surfaces = []
		self.inscriptions = []

		# Create interface objects
		self.createInscription("Projects", "Проекты:", (30, 30))

		# Working with the file system
		self.files = os.listdir(os.getcwd() + "/projects/")
		x, y = [30, 40]
		for i in range(len(self.files)):
			y += 40
			self.createLink("link_" + str(i), self.files[i], (x, y), "/" + self.files[i] + "/")

	# Create link
	def createLink(self, name, value, xy, rtrn):
		link = Link(name, value, xy, rtrn)
		self.links.append(link)

	# Create button
	def createButton(self):
		pass

	# Create surface
	def createSurface(self, name, alpha, xy, wh):
		surface = Surface(name, alpha, xy, wh)
		self.surfaces.append(surface)

	# Create inscription
	def createInscription(self, name, value, xy):
		inscription = Inscription(name, value, xy)
		self.inscriptions.append(inscription)

	# Rendering launcher interface objects
	def drawObjects(self, screen):
		# Rendering links
		for link in self.links:
			link.draw(screen)
		# Rendering buttons
		for button in self.buttons:
			button.draw(screen)
		# Rendering surfaces
		for surface in self.surfaces:
			surface.draw(screen)
		# Rendering inscriptions
		for inscription in self.inscriptions:
			inscription.draw(screen)
