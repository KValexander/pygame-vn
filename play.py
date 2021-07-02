# Connecting libraries
import pygame
import codecs
import sys
import os
import re

# Connecting files
from settings import *
from storage import *
from other import *

# Play class
class Play:
	def __init__(self, screen, folder, loop):
		self.screen = screen
		self.folder = folder
		self.loop 	= loop

	# Loading data
	def loading(self):
		# Getting dialog box
		for surface in surfaces:
			if surface.name == "dialogbox":
				self.dialogbox = surface

		# Option variables
		self.textmargin = 0
		self.textsize  	= 0
		self.textcolor	= ()
		self.textfont	= ""
		self.lineheight = 0

		# Parsing the option file
		self.parseOption()

		# Variables of text
		self.textprint  = pygame.font.SysFont(self.textfont, self.textsize)
		self.textwidth 	= (self.dialogbox.xy[0] + self.dialogbox.wh[0]) - (self.textmargin * 2)
		self.textheight = (self.dialogbox.xy[1] + self.dialogbox.wh[1]) - (self.textmargin * 2)
		self.textsize 	= (self.textwidth, self.textheight)

		# Variables text name
		self.name 		= ""
		self.namekey 	= ""
		self.nameshow 	= False
		self.namecolor  = (0,0,0)
		self.namepos 	= (self.textmargin, HEIGHT - (HEIGHT / 4))
		self.nameprint  = self.textprint.render(str(self.name), True, self.namecolor)

		# Line counting variables
		self.currentStart = 0
		self.currentEnd   = 0

		# Variable lines
		self.allLines 	  = []
		self.currentLine  = ""
		self.currentLines = []

		# Variable commands
		self.variables  = []
		self.counters 	= {}
		self.names 			= {}
		self.names["name"] 	= {}
		self.names["color"] = {}
		self.characters 		 = {}
		self.characters["src"] 	 = {}
		self.characters["coord"] = {}

		# Rendering variables
		self.renderCharacters = {}

		# Boolean variables
		self.hide = False
		self.choice = False

		# Condition variables
		self.condition = ""
		self.conditionxy = ()
		self.conditionwh = ()
		self.conditionSize = ()
		self.conditionmargin = 10
		self.clauses = {}
		self.clausesxy = {}
		self.clausesprint = {}

		# Other variables
		self.mouse = ()

		# Standard background image
		self.background = scLoadImage(self.folder + "assets/gui/backgroundplay.jpg", SIZE)

		# Parsing the script file
		self.parseScript()

	# Parsing the option file
	def parseOption(self):
		# Getting option content
		option = codecs.open(self.folder + "options.vn", "r", "utf-8")
		content = option.read()

		# Splitting a option
		define = content.split(";")
		
		# Getting options
		for val in define:
			arr = val.split("=")
			name, value = arr[0], arr[1]
			if name.find("textmargin") != -1:
				self.textmargin = int(value)
			if name.find("textsize") != -1:
				self.textsize = int(value)
			if name.find("textcolor") != -1:
				self.textcolor = self.defineColor(value)
			if name.find("textfont") != -1:
				self.textfont = value
			if name.find("lineheight") != -1:
				self.lineheight = int(value)

	# Define color
	def defineColor(self, color):
		result = ()
		if color == "WHITE": result = WHITE
		elif color == "BLACK": result = BLACK
		else:
			color = removeChar(color)
			arr = color.split(",")
			result = (int(arr[0]), int(arr[1]), int(arr[2]))
		return result

	# Define coordinates
	def defineCoord(self, coord):
		coord = coord.replace(" ", "")
		coord = removeChar(coord).split(";")
		if float(coord[0]) == 0.0: x = 0
		else: x = WIDTH * float(coord[0])
		if float(coord[1]) == 0.0: y = 0
		else: y = HEIGHT * float(coord[1])
		coord = (x, y)
		return coord

	# Parsing the script file
	def parseScript(self):
		# Getting script content
		script = codecs.open(self.folder + "script.vn", "r", "utf-8")
		content = script.read()

		# Splitting a script
		define = content.split("start:")

		# Cleaning chars 
		badChars = ['\r', '\n', '\t']

		# Script variables
		self.variables = define[0].split("\n")
		# Script all lines
		self.allLines = define[1].split("\n")

		# Clearing script variables
		for i in range(len(self.variables)):
			for char in badChars:
				self.variables[i] = self.variables[i].replace(char, "")

		# Clearing script all lines
		for i in range(len(self.allLines)):
			for char in badChars:
				self.allLines[i] = self.allLines[i].replace(char, "")

		# Clearing empty list items
		self.variables = [x for x in self.variables if x != '']
		self.allLines = [x for x in self.allLines if x != '']
		
		# End of lines
		self.currentEnd = len(self.allLines) - 1

		self.variablesProcessing()
		self.linesProcessing()

	# Processing script variables
	def variablesProcessing(self):
		for var in self.variables:
			# Name variables
			if var.find("name") != -1:
				var = clearVariable(var, "name")
				name, value = var[0], removeChar(var[1]).split(",")
				self.names["name"][name] = removeChar(value[0])
				self.names["color"][name] = value[1]
			# Characters variables
			elif var.find("character") != -1:
				var = clearVariable(var, "character")
				name, value = var[0], removeChar(var[1]).split(",")
				self.characters["src"][name] = removeChar(value[0])
				self.characters["coord"][name] = self.defineCoord(value[1])
			# Counter variables
			elif var.find("count") != -1:
				var = clearVariable(var, "count")
				name, value = var[0], var[1]
				self.counters[name] = int(value)

	# Processing script all lines
	def linesProcessing(self):
		# If all the lines are finished
		if(self.currentStart > self.currentEnd):
			self.loop.running = False
			return

		# If there is no current line
		if self.currentStart <= 0: self.currentStart = 0

		# Current line
		self.currentLine = self.allLines[self.currentStart]
		print(self.currentLine)

		# If current line = return
		if self.currentLine == "return":
			self.loop.running = False
			return

		# If this is a replica without name
		if self.currentLine[0] == "\"" or self.currentLine[0] == "\'":
			self.currentLine = removeChar(self.currentLine)
			self.nameshow = False
			self.setLine()
		# Else this is a commands
		else:
			# Command processing
			self.commandProcessing()

	# Command processing
	def commandProcessing(self):
		# Getting a command
		define = self.currentLine.split(" ")
		command = define[0]
		i = 0

		# Check comments
		if command == "#":
			return self.nextLine()

		# Check names
		elif command in self.names["name"]:				
			self.currentLine = self.currentLine.split("\"")
			self.currentLine = self.currentLine[1]
			self.setLine()

			self.nameshow = True
			self.namekey = command
			return self.setName()

		# Set background
		elif command == "background":
			src = self.folder + "/assets/images/medley/" + removeChar(define[1])
			if os.path.exists(src) == False:
				src = self.folder + "/assets/gui/backgroundplay.jpg"
			self.background = scLoadImage(src, SIZE)

		# Show characters
		elif command == "show":
			if define[1] in self.characters["src"]:
				src = self.folder + "/assets/images/characters/" + self.characters["src"][define[1]]
				if os.path.exists(src) == False:
					src = self.folder + "/assets/gui/characterstock.png"
			else:
				src = self.folder + "/assets/gui/characterstock.png"
			self.renderCharacters[define[1]] = loadImage(src)

		# Hide characters
		elif command == "hide":
			if define[1] in self.renderCharacters:
				self.renderCharacters.pop(define[1])

		# Checking variable counters
		elif command == "if":
			check = self.currentLine.replace("if", "")
			check = check.split(":")
			check[0] = check[0].replace(" ", "")
			if self.ifCheck(check[0]):
				self.ifProcessing(check[1])

		# Dialogue condition
		elif command == "condition":
			# Getting a condition
			self.condition = self.currentLine.replace("condition", "")
			if self.condition.find(":") != -1:
				self.condition = removeChar(removeChar(self.condition))
				self.clauses.clear()
				self.clausesprint.clear()
				# Getting condition clauses
				for n in range(999):
					self.currentStart += 1
					self.currentLine = self.allLines[self.currentStart]
					if self.currentLine.find(":") != -1:
						arr = self.currentLine.split(":")
						name, value = arr[0], arr[1]
						self.clauses[name] = value
					else:
						self.currentStart -= 1
						break
				# Working with a condition
				return self.setCondition()

		# Go to label
		elif command == "go!":
			# Find label in all lines and go to it
			for line in self.allLines:
				if line.find("label") != -1:
					label = line.replace("label", "")
					label = label.replace(" ", "")
					if label == define[1] + ":":
						self.currentStart = i
						break
				i += 1

		self.nextLine()

	# Variable Validation check
	def ifCheck(self, check):
		arrcond = ["==", "<=", ">=", "<", ">", "!="]
		for i in range(len(arrcond)):
			if check.find(arrcond[i]) != -1:
				cond = check.split(arrcond[i])
				if cond[0] in self.counters: cond[0] = self.counters[cond[0]]
				else: cond[0] = int(cond[0])
				if cond[1] in self.counters: cond[1] = self.counters[cond[1]]
				else: cond[1] = int(cond[1])

				# If possible, this should be optimized.
				if arrcond[i] == "==":
					if cond[0] == cond[1]: return True
				elif arrcond[i] == "<=":
					if cond[0] <= cond[1]: return True
				elif arrcond[i] == ">=":
					if cond[0] >= cond[1]: return True
				elif arrcond[i] == "<":
					if cond[0] < cond[1]: return True
				elif arrcond[i] == ">":
					if cond[0] > cond[1]: return True
				elif arrcond[i] == "!=":
					if cond[0] != cond[1]: return True
				else: return False

	# Variable Validation Handling
	def ifProcessing(self, commands):
		commands = commands.split(" ")
		commands = [x for x in commands if x != '']
		i = 0

		# Handling commands
		for command in commands:
			# Yes, this code is repeated almost three times. There is something to optimize
			if command == "go!":
				for line in self.allLines:
					if line.find("label") != -1:
						label = line.replace("label", "")
						label = label.replace(" ", "")
						if label == commands[1] + ":":
							self.currentStart = i - 1
							break
					i += 1

	# Condition decision processing
	def conditionProcessing(self, claus):
		commands = self.clauses[claus].split(";")
		i, j, l = 0, 0, 0

		# Handling commands
		for command in commands:
			cmd = command.split(" ")
			cmd = [x for x in cmd if x != '']
			for c in cmd:

				# Go to label
				if c == "go!":
					for line in self.allLines:
						if line.find("label") != -1:
							label = line.replace("label", "")
							label = label.replace(" ", "")
							if label == cmd[1] + ":":
								self.currentStart = l
								self.choice = False
								self.linesProcessing()
								return
						l += 1

				# Continuation of the current label dialog
				if c == "continue":
					self.choice = False

				# Increase counter
				for counter in self.counters:
					if counter + "++" == c:
						self.choice = False
						self.counters[counter] += 1
				j += 1
			i += 1

		self.nextLine()


	# Moving the script line forward
	def nextLine(self):
		self.currentStart += 1
		self.linesProcessing()

	# Moving the script line back
	def prevLine(self):
		self.currentStart -= 1
		self.linesProcessing()

	# Handling events
	def events(self, e):
		# Handling mouse click
		if e.type == pygame.MOUSEBUTTONDOWN:

			if self.hide == False and self.choice == False:
				# Left mouse button
				if e.button == 1:
					self.nextLine()
				
				# Move the mouse wheel forward
				if e.button == 4:
					self.prevLine()

				# Move the mouse wheel back
				if e.button == 5:
					self.nextLine()

			if self.choice:
				if e.button == 1:
					# Selecting a clauses condition
					xy = [self.conditionxy[0], self.conditionxy[1]]
					for claus in self.clausesprint:
						xy[1] += self.textmargin * 2
						if mouseCollision((xy[0], xy[1]), self.conditionwh, e.pos):
							self.conditionProcessing(claus)

			# Right mouse button
			if e.button == 3:
				if self.hide == True: self.hide = False
				elif self.hide == False: self.hide = True

		# Handling mouse move
		if e.type == pygame.MOUSEMOTION:
			self.mouse = e.pos

	# Rendering objects
	def draw(self):
		# Rendering background
		drawImage(self.screen, self.background, (0, 0))

		# Rendering characters
		for character in self.renderCharacters:
			xy = (WIDTH / 2 - 300, HEIGHT / 2 - 300)
			if character in self.characters["coord"]:
				xy = self.characters["coord"][character]
			self.screen.blit(self.renderCharacters[character], xy)

		if self.hide == False:
			# Rendering dialogbox
			self.dialogbox.draw(self.screen)
			# Rendering text
			self.outLine(self.screen)

		if self.choice:
			rectxy = (self.conditionxy[0] - self.conditionmargin, self.conditionxy[1] - self.conditionmargin / 2)
			rectwh = (self.conditionwh[0] + self.conditionmargin * 2, self.conditionwh[1] + self.conditionmargin)
			# Rendering condition
			pygame.draw.rect(self.screen, BLACK, ((rectxy), (rectwh)))
			self.screen.blit(self.condition, self.conditionxy)
			# Rendering clauses
			yy = [self.conditionxy[1], rectxy[1]]
			for claus in self.clausesprint:
				yy[0] += self.textmargin * 2
				yy[1] += self.textmargin * 2
				pygame.draw.rect(self.screen, BLACK, ((rectxy[0], yy[1]), (rectwh)))
				self.screen.blit(self.clausesprint[claus], (self.clausesxy[claus][0], yy[0]))

				if mouseCollision((rectxy[0], yy[1]), (rectwh), self.mouse):
					pygame.draw.rect(self.screen, SURFACECOLOR, ((rectxy[0], yy[1]), (rectwh)), 3)

	# Set name
	def setName(self):
		self.name = self.names["name"][self.namekey]
		self.namecolor = self.defineColor(self.names["color"][self.namekey])
		self.nameprint = self.textprint.render(str(self.name), True, self.namecolor)

	# Set condition
	def setCondition(self):
		self.choice = True
		self.conditionSize = self.textprint.size(self.condition)
		self.condition = self.textprint.render(str(self.condition), True, self.textcolor)
		self.conditionxy = (WIDTH / 2 - self.conditionSize[0] / 2, HEIGHT / 2 - self.conditionSize[1] * 3)
		self.conditionwh = self.condition.get_size()
		
		for claus in self.clauses:
			cl = self.textprint.render(str(claus), True, self.textcolor)
			clxy = self.textprint.size(claus)
			self.clausesxy[claus] = (WIDTH / 2 - clxy[0] / 2, HEIGHT / 2 - clxy[0] / 2)
			self.clausesprint[claus] = cl

	# Set line text
	def setLine(self):
		self.currentLines.clear()
		for text in self.processingLine():
			line = self.textprint.render(str(text), True, self.textcolor)
			self.currentLines.append(line)

	# Line text processing
	def processingLine(self):
		lines = []
		words = self.currentLine.split(" ")
		count = len(words)
		line = ""

		for i in range(count):
			textline = line + words[i] + " "
			textwh = self.textprint.size(textline)
			if textwh[0] > self.textwidth:
				lines.append(line)
				line = words[i] + " "
			else:
				line = textline
			if i == count - 1:
				lines.append(line)

		return lines

	# Output a line of text
	def outLine(self, screen):
		# Rendering a line of text
		x, y = self.textmargin, HEIGHT - (HEIGHT / 4) + (self.textmargin * 2)
		for line in self.currentLines:
			screen.blit(line, (x, y))
			y += self.lineheight

		# Rendering name
		if self.nameshow:
			screen.blit(self.nameprint, self.namepos)
