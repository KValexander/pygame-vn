# Including pygame library
import pygame

# Connect files
from configs import *
from arrays import *
from collisions import *

# Mouse class
class Mouse:
	def __init__(self):
		self.coordClick = (0, 0)
		self.clickX 	= 0
		self.clickY 	= 0

		self.coordMove 	= (0, 0)
		self.moveX 		= 0
		self.moveY 		= 0

	# Handling mouse down
	def mouseDown(self, e):
		self.clickX, self.clickY = e.pos
		self.coordClick = e.pos
		# Set movement items
		if(e.button == 3):
			for item in selectedItems:
				item.setMove(self.clickX - item.rect.width / 2, self.clickY - item.rect.height / 2)

	# Handling mouse up
	def mouseUp(self, e):
		return 0

	# Handling mouse move
	def mouseMove(self, e):
		self.moveX, self.moveY = e.pos
		self.coordMove = e.pos

# Keys class
class Key:
	def __init__(self):
		self.code = 0

	# Handling key down
	def keyDown(self, e):
		self.code = e.key
		print(e.key)
		if self.code == pygame.K_DELETE:
			removeItems()

	# Handling key up
	def keyUp(self, e):
		self.code = 0

# Cash class
class Cash:
	def __init__(self):
		self.gold 	= 0
		self.wood 	= 0
		self.metal 	= 0
		self.food 	= 0

	# Set Cash
	def setCash(self, gold, wood, metal, food):
		self.gold 	= gold
		self.wood	= wood
		self.metal 	= metal
		self.food 	= food

	# Give Cash
	def giveCash(self, gold, wood, metal, food):
		self.gold 	+= gold
		self.wood 	+= wood
		self.metal 	+= metal
		self.food 	+= food

# Grid class
class Grid:
	def __init__(self):
		self.color 	= (230, 230, 230)
		self.i 		= 0
		self.lineX 	= GRIDLINEX
		self.lineY 	= GRIDLINEY
		self.collsX = WIDTH / self.lineX
		self.collsY = HEIGHT / self.lineY
		self.conditionX = self.collsX * self.lineX
		self.conditionY = self.collsY * self.lineY

	# Casting numbers to multiples of the grid
	def gridSize(self, n, case):
		if case == "x": n = int(n / GRIDLINEX) * GRIDLINEX
		if case == "y": n = int(n / GRIDLINEY) * GRIDLINEY
		return n

	# Method grid rendering
	def drawGrid(self, screen):
		while self.i <= self.conditionX:
			pygame.draw.line(screen, self.color, (self.i, 0), (self.i, HEIGHT))
			self.i += self.lineX
		self.i = 0
		while self.i <= self.conditionY:
			pygame.draw.line(screen, self.color, (0, self.i), (WIDTH, self.i))
			self.i += self.lineY
		self.i = 0
		
# Camera class
class Camera:
	def __init__(self, width, height):
		pass

# Fog class
class Fog:
	def __init__(self):
		self.color = BLACK
		self.lX = GRIDLINEX
		self.lY = GRIDLINEY
		self.cX = WIDTH / self.lX
		self.cY = HEIGHT / self.lY
		self.conditionX = self.cX * self.lX
		self.conditionY = self.cY * self.lY
		self.surface = pygame.Surface([self.lX, self.lY])
		self.surface.fill(self.color)

	def drawFog(self, screen):
		for i in range(int(self.conditionX)):
			if i % self.lX == 0:
				for j in range(int(self.conditionY)):
					if j % self.lY == 0:
						self.surface.set_alpha(200)
						for item in items:
							if(fogCollision(item, i, j, self.lX, self.lY) == True):
								self.surface.set_alpha(0)
						screen.blit(self.surface, (i, j))


# Items selection rectangle
class SelectionRect:
	def __init__(self):
		self.lineWidth  = 2
		self.color  	= GREEN
		self.x 			= 0
		self.y 			= 0
		self.width 		= 0
		self.height 	= 0
		self.state 		= False

	# Update data
	def update(self, click, move):
		cX, cY = click
		mX, mY = move
		self.x = cX
		self.y = cY
		self.width = mX - cX
		self.height = mY - cY

	# Rendering selection rectangle
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], self.lineWidth)

	# Clear data
	def clear(self):
		self.x 		= 0
		self.y 		= 0
		self.width 	= 0
		self.height = 0
		self.state 	= False

	# Adding items in selected items
	def selection(self):
		# Clear selected items
		clearSelection()

		# Adding selected items
		for item in items:
			if selectCollision(self, item):
				addSelection(item)

		# Clear selection rectangle
		self.clear()