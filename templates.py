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
# 	Cells
# 	Texture
# 	Surface
# 	Inscription

# class Icon
class Icon:
	def __init__(self, name, src, xy, wh, folder, srcstock):
		# Custom variables
		self.name 	= name
		self.src  	= src
		self.xy   	= xy
		self.wh   	= wh
		self.folder = folder
		self.srcstock = srcstock

		# Boolean variables
		self.hide 		= False
		self.hover 		= False
		self.selected 	= False
		self.setHover 	= False

		# Default variables
		self.hoverImage = ""
		self.pathToImageHover = ""
		self.pathToImage = self.folder + self.src
		if os.path.exists(self.pathToImage) == False:
			self.pathToImage = self.srcstock
		if self.wh != None:self.image = scLoadImage(self.pathToImage, self.wh)
		else: self.image = loadImage(self.pathToImage)
		self.rect = self.image.get_rect()
		self.wh = (self.rect.width, self.rect.height)

	# Rendering icon
	def draw(self, window):
		if self.hover == False:
			window.blit(self.image, self.xy)
		else: window.blit(self.hoverImage, self.xy)

	# Set hover image
	def setHoverImage(self, src):
		if self.setHover == False:
			self.setHover = True
			self.pathToImageHover = self.folder + src
			if os.path.exists(self.pathToImageHover) == False:
				self.pathToImageHover = self.srcstock
			self.hoverImage = scLoadImage(self.pathToImageHover, self.wh)

# class Link
class Link:
	def __init__(self, name, value, xy, color, aim, selected, size, font, typefont):
		# Custom variables
		self.name 			= name
		self.value 			= str(value)
		self.xy 			= xy
		self.color 			= color
		self.coloraim 		= aim
		self.colorselected  = selected
		self.size 			= size
		self.typefont 		= typefont

		# Boolean variables
		self.hide 		= False
		self.hover 		= False
		self.selected 	= False

		# Font variable
		if self.typefont == "system":
			self.font = pygame.font.SysFont(font, self.size)
		elif self.typefont == "own":
			if os.path.exists(font):
				self.font = pygame.font.Font(font, self.size)
			else: self.font = pygame.font.SysFont("calibri", self.size)
		else: self.font = pygame.font.SysFont("calibri", self.size)

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
	def __init__(self, name, value, xy, width, color, size, lh, font, typefont):
		# Custom variables
		self.name 		= name
		self.value 		= str(value)
		self.xy 		= xy
		self.width 		= width
		self.color 		= color
		self.size 		= size
		self.lh 		= lh
		self.typefont	= typefont
		self.y 			= xy[1]

		# Boolean variables
		self.hide = False

		# Font variable
		if self.typefont == "system":
			self.font = pygame.font.SysFont(font, self.size)
		elif self.typefont == "own":
			if os.path.exists(font):
				self.font = pygame.font.Font(font, self.size)
			else: self.font = pygame.font.SysFont("calibri", self.size)
		else: self.font = pygame.font.SysFont("calibri", self.size)

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

# class Cells
class Cells:
	def __init__(self, xy, wh, font, typefont, horiz, vert, pages, backcol, outline, border, alpha, margin, tcolor, tsize):
		# Custom variables
		self.xy 					= xy
		self.wh 					= wh
		self.typefont 				= typefont

		if horiz == None: horiz 	= 3
		self.horizontally 			= horiz

		if vert == None: vert 		= 2
		self.vertically 			= vert

		if pages == None: pages 	= "auto"
		elif pages != "auto": pages = int(pages)
		self.pages 					= pages

		if backcol == None: backcol = (0,0,0) 
		self.backgroundcolor 		= backcol

		if outline == None: outline = (255,255,255) 
		self.outline 				= outline

		if border == None: border 	= 3 
		self.border 				= border

		if alpha == None: alpha 	= 140
		self.alpha 					= alpha

		if margin == None: margin 	= 10
		self.margin 				= margin

		if tcolor == None: tcolor 	= (255,255,255)
		self.tcolor 				= tcolor

		if tsize == None: tsize 	= 20
		self.tsize 					= tsize

		# Font variable
		if self.typefont == "system":
			self.font = pygame.font.SysFont(font, self.tsize)
		elif self.typefont == "own":
			if os.path.exists(font):
				self.font = pygame.font.Font(font, self.tsize)
			else: self.font = pygame.font.SysFont("calibri", self.tsize)
		else: self.font = pygame.font.SysFont("calibri", self.tsize)

		# Default variables
		self.page = 0
		self.cells = []
		self.textstock = "Пусто"
		self.twh = self.font.size(self.textstock)
		self.print = self.font.render(self.textstock, True, self.tcolor)
		self.cellsonpage = self.horizontally * self.vertically
		self.mwh = self.wh[0] - (self.margin * self.horizontally - self.margin), self.wh[1] - (self.margin * self.vertically - self.margin)
		# Cells width/height
		self.cwh = self.mwh[0] / self.horizontally, self.mwh[1] / self.vertically
		# Text stock x/y
		self.txy = (self.xy[0] + self.cwh[0] / 2 - self.twh[0] / 2, self.xy[1] + self.cwh[1] / 2 - self.twh[1] / 2)

		self.setPage(0)

	# Set page
	def setPage(self, page):
		self.page = page
		self.createCells()

	# Create cell
	def createCells(self):
		self.cells.clear()
		x, y = self.xy
		tx, ty = self.txy
		surface = pygame.Surface(self.cwh)
		surface.fill(self.backgroundcolor)
		surface.set_alpha(self.alpha)
		for i in range(self.cellsonpage):
			name = "cell_" + str(self.page) + "_" + str(i)
			if i % self.horizontally == 0 and i != 0:
				y += self.cwh[1] + self.margin
				ty += self.cwh[1] + self.margin
				x = self.xy[0]
				tx = self.txy[0]
			elif i != 0:
				x += self.cwh[0] + self.margin
				tx += self.cwh[0] + self.margin
			cell = {
				"name": name,
				"xy": (x,y),
				"wh": self.cwh,
				"txy": (tx, ty),
				"text": self.print,
				"surface": surface,
				"hover": False,
				"workload": False
			}

			self.cells.append(cell)

		# Check cells for saving
		self.checkCells()

	# Check cells for saving
	def checkCells(self):
		pass

	# Draw cells
	def draw(self, window):
		for cell in self.cells:
			window.blit(cell["surface"], cell["xy"])
			window.blit(cell["text"], cell["txy"])
			if cell["hover"]:
				pygame.draw.rect(window, self.outline, (cell["xy"], cell["wh"]), self.border)

# class Texture
class Texture:
	def __init__(self, name, src, xy, wh, folder, srcstock):
		# Custom variables
		self.name 	= name
		self.src  	= src
		self.xy   	= xy
		self.wh   	= wh
		self.folder = folder
		self.srcstock = srcstock

		# Boolean variables
		self.hide = False

		# Default variables
		self.pathToImage = self.folder + self.src
		if os.path.exists(self.pathToImage) == False:
			self.pathToImage = self.srcstock
		self.image = scLoadImage(self.pathToImage, self.wh)
		self.rect = self.image.get_rect()

	# Rendering icon
	def draw(self, window):
		window.blit(self.image, self.xy)

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
	def __init__(self, name, value, xy, color, size, font, typefont):
		# Custom variables
		self.name 	= name
		self.value 	= value
		self.color 	= color
		self.size 	= size
		self.xy 	= xy
		self.typefont = typefont
		# Font variable
		if self.typefont == "system":
			self.font = pygame.font.SysFont(font, self.size)
		elif self.typefont == "own":
			if os.path.exists(font):
				self.font = pygame.font.Font(font, self.size)
			else: self.font = pygame.font.SysFont("calibri", self.size)
		else: self.font = pygame.font.SysFont("calibri", self.size)

		# Defaults variables
		self.twh 	= self.font.size(self.value)
		self.iname 	= self.font.render(str(self.value), True, self.color)
		self.rect 	= self.iname.get_rect()

	# Inscription rendering
	def draw(self, window):
		window.blit(self.iname, self.xy)