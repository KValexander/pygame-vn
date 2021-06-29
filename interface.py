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
	def __init__(self):
		pass

# Interface class
class Interface:
	def __init__(self, screen):
		self.screen = screen
		self.create()

	# Create button
	def createButton(self, name, value, tcolor, xy, wh, bcolor):
		button = Button(name, value, tcolor, xy, wh, bcolor)
		buttons.append(button)

	# Create surface
	def createSurface(self):
		pass

	# Create objects
	def create(self):
		self.createSurface()

		self.createButton("start", "Начать игру", WHITE, gridSize((60, 50)), (180, 40), QUARTZ)
		self.createButton("exit", "Выйти", WHITE, gridSize((60, HEIGHT - 100)), (180, 40), QUARTZ)

	# Handling events
	def events(self, e, btnAct):
		# Handling button events
		for button in buttons:
			# Handling button click
			if e.type == pygame.MOUSEBUTTONDOWN:
				if button.rect.collidepoint(e.pos):
					btnAct(button.name)

			# Hovering over the button
			if e.type == pygame.MOUSEMOTION:
				if(button.rect.collidepoint(e.pos)):
					button.hover = True
				else: button.hover = False

	# Rendering objects
	def draw(self):
		# Rendering buttons
		for button in buttons:
			button.draw(self.screen)

	# Calculating object data
	def update(self):
		pass