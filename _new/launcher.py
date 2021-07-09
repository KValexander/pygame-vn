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
# 	Launcher

# Link class
class Link:
	def __init__(self, name, value, xy, rtrn):
		# Custom variables
		self.name 	= name
		self.value 	= str(value)
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
		self.margin 		= LINKMARGIN
		self.size 			= TEXTLINKSIZE
		self.sysfont 		= pygame.font.SysFont(TEXTSYSFONT, self.size)
		self.ownfont 		= pygame.font.Font(TEXTOWNFONT, self.size)
		self.twh 			= self.ownfont.size(self.value)
		self.iname 			= self.ownfont.render(self.value, True, self.color)
		self.rect 			= self.iname.get_rect()
		self.surfacerect 	= [self.xy[0] - self.margin, self.xy[1] - 5, self.twh[0] + self.margin * 2, self.twh[1] + 10]

	# Rendering link
	def draw(self, window):
		if self.hover:
			pygame.draw.rect(window, LINKHOVERSURFACE, self.surfacerect)
			self.iname = self.ownfont.render(self.value, True, self.coloraim)
		else: self.iname = self.ownfont.render(self.value, True, self.color)
		
		if self.selected:
			pygame.draw.rect(window, LINKSELECTEDSURFACE, self.surfacerect)
			self.iname = self.ownfont.render(self.value, True, self.colorselected)

		window.blit(self.iname, self.xy)

	# Select link
	def select(self):
		self.selected = True

# Button class
class Button:
	def __init__(self, name, value, xy, wh):
		# Custom variables
		self.name 	= name
		self.value 	= str(value)
		self.xy 	= xy
		self.wh 	= wh

		# Boolean variables
		self.click = False
		self.hover = False

		# Default variables
		self.colorbutton 	= BUTTON 
		self.colortext 		= TEXTBUTTON
		self.coloraim		= TEXTBUTTONAIM
		self.coloroverline 	= BUTTONOVERLINE
		self.size 			= TEXTBUTTONSIZE
		self.sysfont 		= pygame.font.SysFont(TEXTSYSFONT, self.size)
		self.ownfont 		= pygame.font.Font(TEXTOWNFONT, self.size)
		self.twh 			= self.ownfont.size(self.value)
		self.loc 			= (self.xy[0] + self.wh[0] / 2 - self.twh[0] / 2, self.xy[1] + self.wh[1] / 2 - self.twh[1] / 2)
		self.rect 			= pygame.Rect((self.xy), (self.wh))
		self.iname 			= self.ownfont.render(self.value, True, self.colortext)

	# Rendering button
	def draw(self, window):
		pygame.draw.rect(window, self.colorbutton, self.rect)

		if self.hover == True:
			pygame.draw.rect(window, self.coloroverline, self.rect, 3)
			self.iname = self.ownfont.render(self.value, True, self.coloraim)
		else: self.iname = self.ownfont.render(self.value, True, self.colortext)

		window.blit(self.iname, self.loc)

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
	def draw(self, window):
		window.blit(self.surface, self.xy)

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
	def draw(self, window):
		window.blit(self.iname, self.xy)

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
		self.createSurface("line", 255, (20, 30), (180, 40))
		self.createButton("startproject", "Запустить проект", (WIDTH - 300, HEIGHT - 100), (250, 50))
		self.createButton("createproject", "Создать проект", (WIDTH - 250, HEIGHT - 160), (200, 40))
		self.createButton("updatelistcprojects", "Обновить список", (WIDTH - 250, HEIGHT - 210), (200, 40))
		self.createButton("deleteproject", "Удалить проект", (WIDTH - 250, HEIGHT - 260), (200, 40))

		# Create project list
		self.createProjectList()

	# Create project list
	def createProjectList(self):
		self.links.clear()
		self.files = os.listdir(os.getcwd() + "/projects/")
		x, y = [30, 50]
		for i in range(len(self.files)):
			y += 35
			self.createLink("link_" + str(i), self.files[i], (x, y), "/" + self.files[i] + "/")


	# Create link
	def createLink(self, name, value, xy, rtrn):
		link = Link(name, value, xy, rtrn)
		self.links.append(link)

	# Create button
	def createButton(self, name, value, xy, wh):
		button = Button(name, value, xy, wh)
		self.buttons.append(button)

	# Create surface
	def createSurface(self, name, alpha, xy, wh):
		surface = Surface(name, alpha, xy, wh)
		self.surfaces.append(surface)

	# Create inscription
	def createInscription(self, name, value, xy):
		inscription = Inscription(name, value, xy)
		self.inscriptions.append(inscription)
	
	# Draw line
	def drawLine(self, window, color, spos, epos, lw):
		pygame.draw.line(window, color, spos, epos, lw)

	# Rendering launcher interface objects
	def drawObjects(self, window):

		# Rendering links
		for link in self.links:
			link.draw(window)
		# Rendering buttons
		for button in self.buttons:
			button.draw(window)
		# Rendering surfaces
		for surface in self.surfaces:
			surface.draw(window)
		# Rendering inscriptions
		for inscription in self.inscriptions:
			inscription.draw(window)
