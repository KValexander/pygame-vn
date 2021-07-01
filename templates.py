# Including pygame library
import pygame

# Connecting libraries
import random
import time
import threading

# Connecting files
from configs import *
from arrays import *
from collisions import *

# Template for units
class Unit():

	# Update
	def update(self):
		self.interaction()
		self.movementTarget()
		self.movement()

	# Line of conduct
	def lineConduct(self, case):
		if case == "stand":
			self.action = "stand"
		elif case == "move":
			self.action = "move"
		elif case == "target":
			self.action = "target"
		elif case == "attack":
			self.action = "attack"
		elif case == "defense":
			self.action = "defense"

	# Draw
	def draw(self, screen):
		if(self.hitPoints <= 0): return removeItem(self)

		if(self.selected == True):
			self.drawMovementLine(screen)

		screen.blit(self.image, self.rect)
		self.drawHealtBar(screen)

		if(self.selected == True):
			self.drawSelection(screen)

	# Draw selection rectangle
	def drawSelection(self, screen):
		if(self.hitPoints > 100): color = GREEN
		elif(self.hitPoints <= 99 and self.hitPoints > 30): color = ORANGE
		elif(self.hitPoints <= 30): color = RED
		pygame.draw.rect(screen, color, [self.rect.x, self.rect.y, self.rect.width, self.rect.height], 2)

		if(self.faction == "red"): color = TEAMRED
		elif(self.faction == "blue"): color = TEAMBLUE
		else: color = GRAY
		pygame.draw.circle(screen, color, self.rect.center, 16, 2)

	# Draw movement line
	def drawMovementLine(self, screen):
		pygame.draw.line(screen, GREEN, self.rect.center, (self.move[0] + self.rect.width / 2, self.move[1] + self.rect.height / 2), 2)

	# Draw health bar
	def drawHealtBar(self, screen):
		rect = [self.rect.x, self.rect.y - 11, self.hitPoints / 5, 5]
		pygame.draw.rect(screen, GREEN, rect)
		pygame.draw.rect(screen, (0, 90, 0), rect, 1)

	# Set motion coordinates
	def setMove(self, x, y):
		self.lineConduct("move")
		self.move = [x, y]

	# Movement items by target
	def movementTarget(self):
		if(self.action != "target" or self.target == 0): return 0
		item = getItemById(self.target)
		if(item == None): return self.stopMove()
		self.move = [item.rect.x, item.rect.y]

	# Movement
	def movement(self):
		if(self.action == "stand" or self.action == "attack" or self.action == "defense"): return 0

		if(self.rect.x < self.move[0]): self.rect.x += self.speed
		if(self.rect.x > self.move[0]): self.rect.x -= self.speed
		if(self.rect.y < self.move[1]): self.rect.y += self.speed
		if(self.rect.y > self.move[1]): self.rect.y -= self.speed

	# Stop motion
	def stopMove(self):
		self.lineConduct("stand")
		self.move = [self.rect.x, self.rect.y,]
		self.target = 0

	# Behavior of items when attacked
	def attackOnEnemy(self, item):
		if(self.action == "move" or self.action == "defense" or self.faction == item.faction): return 0
		if(attackCollision(self, item)):
			if(self.id == item.id): return 0
			self.target = item.id
			self.lineConduct("target")

	# Damage inflicting on the enemy
	def damageOnEnemy(self, item):
		self.timer = False
		if(self.faction == item.faction): return 0
		self.action = "target"
		self.target = item.id
		item.action = "target"
		item.target = self.id
		dmg1 = random.randint(self.damage[0], self.damage[1])
		dmg2 = random.randint(item.damage[0], item.damage[1])
		if(dmg1 <= 0): dmg1 = 0
		if(dmg2 <= 0): dmg2 = 0
		self.hitPoints -= dmg1
		item.hitPoints -= dmg2
		dX = self.cX - item.cX
		dY = self.cY - item.cY
		if(dX > 0): self.rect.x += self.speed
		if(dX < 0): self.rect.x -= self.speed
		if(dY > 0): self.rect.y += self.speed
		if(dY < 0): self.rect.y -= self.speed

	# Actions when colliding with other
	def collisionAction(self, item):
		if itemCollision(self, item):
			dX = self.cX - item.cX
			dY = self.cY - item.cY
			if(dX > 0): self.rect.x += self.speed
			if(dX < 0): self.rect.x -= self.speed
			if(dY > 0): self.rect.y += self.speed
			if(dY < 0): self.rect.y -= self.speed

			self.damageOnEnemy(item)

	# Handling collisions
	def interaction(self):
		for item in items:
			edgesCollision(item)
			# Behavior of items when attacked
			self.attackOnEnemy(item)
			# Handling collisions with each other
			self.collisionAction(item)

class Worker(Unit):
	def __init__(self, ident, x, y, faction):
		# Specified characteristics
		self.id 			= ident
		self.x 				= x
		self.y 				= y
		self.faction		= faction

		# Default characteristics
		self.typeItem 		= "unit"
		self.animationIndex = 0
		self.direction 		= 0
		self.directions 	= 8
		self.speed 			= 2
		self.move 			= [x, y]
		self.target 		= 0
		self.action 		= "stand"
		self.selected 		= False
		self.selectable 	= True

		# Unique characteristics
		self.src 			= "images/worker.png"
		self.name 			= "worker"
		self.iname 			= "Рабочий"
		self.description 	= "Усердный работяга"
		self.hitPoints		= 80
		self.width 			= 16
		self.height 		= 24
		self.gridWidth 		= 1
		self.gridHeight 	= 1.5
		self.damage 		= [5, 7]
		self.defense 		= 1
		self.radius			= 16
		self.sight 			= 32
		self.level 			= 1
		self.maxLevel 		= 1
		self.experiense 	= 0
		self.maxExperiense 	= 0
		self.cost 			= [50, 0, 0, 1]
		self.frames 		= []

		# Calculation
		if(self.faction != "neutral"):
			arr = self.src.split('.')
			self.src = arr[0] + "_" + faction + "." + arr[1]

		# Group characteristic
		self.image 			= pygame.image.load(self.src)
		self.rect 			= self.image.get_rect()
		self.rect.center 	= (x, y)

		# Collisions characteristic
		self.cX = self.rect.x + self.rect.width / 2
		self.cY = self.rect.y + self.rect.height / 2


class Soldier(Unit):
	def __init__(self, ident,  x, y):
		# Specified characteristics
		self.id 			= ident
		self.x 				= x
		self.y 				= y
		self.faction		= faction

		# Default characteristics
		self.typeItem 		= "unit"
		self.animationIndex = 0
		self.direction 		= 0
		self.directions 	= 8
		self.speed 			= 1
		self.move 			= [0, 0]
		self.target 		= 0
		self.action 		= "stand"
		self.selected 		= False
		self.selectable 	= True

		# Unique characteristics
		self.src 			= "images/soldier.png"
		self.name 			= "soldier"
		self.iname 			= "Солдат"
		self.description 	= "Солдат солдатит"
		self.hitPoints		= 160
		self.width 			= 20
		self.height 		= 24
		self.gridWidth 		= 1.25
		self.gridHeight 	= 1.5
		self.damage 		= [11, 15]
		self.defense 		= 3
		self.radius			= 16
		self.sight 			= 32
		self.level 			= 1
		self.maxLevel 		= 3
		self.experiense 	= 0
		self.maxExperiense 	= 500
		self.cost 			= [80, 10, 0, 2]
		self.frames 		= []

		# Calculation
		if(self.faction != "neutral"):
			arr = self.src.split('.')
			self.src = arr[0] + "_" + faction + "." + arr[1]

		# Group characteristic
		self.image 			= pygame.image.load(self.src)
		self.rect 			= self.image.get_rect()
		self.rect.center 	= (x, y)

		# Collisions characteristic
		self.cX = self.rect.x + self.rect.width / 2
		self.cY = self.rect.y + self.rect.height / 2
