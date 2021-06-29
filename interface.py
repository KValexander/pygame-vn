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

# Link class
class Link:
	def __init__(self):
		pass

# Texture class
class Texture:
	def __init__(self):
		pass

# Interface class
class Interface:
	def __init__(self, screen, folder):
		self.screen = screen
		self.folder = folder
		self.create("main")

	# Create button
	def createButton(self, name, value, tcolor, xy, wh, bcolor):
		button = Button(name, value, tcolor, xy, wh, bcolor)
		buttons.append(button)

	# Create surface
	def createSurface(self, name, color, alpha, xy, wh):
		surface = Surface(name, color, alpha, xy, wh)
		surfaces.append(surface)

	# Create link
	def createLink(self):
		pass

	# Create texture
	def createTexture(self):
		pass

	# Create objects
	def create(self, case):
		buttons.clear()
		surfaces.clear()
		dialogues.clear()

		if 	 case == "main": 	 self.createMain()
		elif case == "play": 	 self.createPlay()
		elif case == "settings": self.createSettings()
		elif case == "save": 	 self.createSave()
		elif case == "load": 	 self.createLoad()

	# Create main screen objects
	def createMain(self):
		self.createSurface("startscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
		self.createButton("play", "Начать игру", WHITE, gridSize((60, 200)), (180, 40), QUARTZ)
		self.createButton("load", "Загрузить", WHITE, gridSize((60, 250)), (180, 40), QUARTZ)
		self.createButton("settings", "Настройки", WHITE, gridSize((60, 300)), (180, 40), QUARTZ)
		self.createButton("exit", "Выйти", WHITE, gridSize((60, HEIGHT - 300)), (180, 40), QUARTZ)

	# Create play screen objects
	def createPlay(self):
		self.createSurface("dialogbox", BLACK, 128, gridSize((0, HEIGHT - 200)), gridSize((WIDTH, 216)))

	# Create settings screen objects
	def createSettings(self):
		pass
	# Create load screen objects
	def createLoad(self):
		pass

	# Handling events
	def events(self, e, buttonAction):
		# Handling button events
		for button in buttons:
			# Handling button click
			if e.type == pygame.MOUSEBUTTONDOWN:
				if button.rect.collidepoint(e.pos):
					self.create(buttonAction(button.name))

			# Hovering over the button
			if e.type == pygame.MOUSEMOTION:
				if(button.rect.collidepoint(e.pos)):
					button.hover = True
				else: button.hover = False

	# Rendering objects
	def draw(self):
		# Rendering surfaces
		for surface in surfaces:
			surface.draw(self.screen)

		# Rendering buttons
		for button in buttons:
			button.draw(self.screen)

	# Calculating object data
	def update(self):
		pass