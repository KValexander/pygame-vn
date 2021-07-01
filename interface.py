# Including pygame library
import pygame

# Connecting files
from configs import *
from arrays import *
from collisions import *

# Button class
class Button:
	def __init__(self, name, text, colorT, x, y, w, h, colorB):
		self.name 		 = name
		self.font 		 = pygame.font.SysFont("arial", 20)
		self.text 		 = text
		self.x 			 = x
		self.y 			 = y
		self.width 		 = w
		self.height 	 = h
		self.colorT 	 = colorT
		self.colorB 	 = colorB
		self.colorH 	 = WHITE
		self.tW, self.tH = self.font.size(self.text)
		self.location 	 = (self.x + self.width / 2 - self.tW / 2, self.y + self.height / 2 - self.tH / 2)
		self.rect 		 = pygame.Rect(self.x, self.y, self.width, self.height)
		self.iname 		 = self.font.render(str(self.text), True, self.colorT)

	def draw(self, screen, mouse):
		pygame.draw.rect(screen, self.colorB, self.rect, 0)
		screen.blit(self.iname, self.location)

		if(mouseCollision(self, mouse.coordMove)):
			self.hoverDraw(screen)

	def hoverDraw(self, screen):
		pygame.draw.rect(screen, self.colorH, self.rect, 1)

# Surface class
class Surface:
	def __init__(self, name, color, alpha, x, y, width, height):
		self.name 				= name
		self.color 				= color
		self.alpha 				= alpha
		self.x 					= x
		self.y 					= y
		self.width 				= width
		self.height 			= height
		self.location 			= (self.x, self.y)
		self.size				= (self.width, self.height)
		self.surface 			= pygame.Surface(self.size)
		self.surface.fill(self.color)
		self.surface.set_alpha(self.alpha)

	def draw(self, screen):
		screen.blit(self.surface, self.location)
		self.drawBorder(screen)

	def drawBorder(self, screen):
		pygame.draw.rect(screen, WHITE, [self.x, self.y, self.width, self.height], 1)

# Menu class
class Menu:
	def __init__(self):
		pass

# Interface class
class Interface:
	def __init__(self, screen):
		self.screen = screen
		self.menuScreen = False
		self.create()

	# Create button
	def createButton(self, name, text, colorT, x, y, w, h, colorB):
		button = Button(name, text, colorT, x, y, w, h, colorB)
		buttons.append(button)
	
	# Create surface
	def createSurface(self, name, color, alpha, x, y, width, height):
		surface = Surface(name, color, alpha, x, y, width, height)
		surfaces.append(surface)

	def createTexture(self):
		pass

	# Creating interface elements 
	def create(self):
		clearButtons()
		clearSurfaces()

		self.createSurface("srfc", BLACK, 110, 8, 8, 344, 48)
		self.createButton("button", "button", WHITE, 184, 16, 160, 32, BLACK)
		self.createButton("menu", "Меню", WHITE, 16, 16, 160, 32, BLACK)

	# Draw interface
	def draw(self, mouse):
		# Draw surfaces
		for surface in surfaces:
			surface.draw(self.screen)

		# Draw buttons
		for button in buttons:
			button.draw(self.screen, mouse)

	def update(self):
		pass
