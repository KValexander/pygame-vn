# Connecting libraries
import pygame
import codecs
import sys
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
		self.textloc 	= (self.textmargin, HEIGHT - (HEIGHT / 4) + self.textmargin)
		self.textwidth 	= (self.dialogbox.xy[0] + self.dialogbox.wh[0]) - (self.textmargin * 2)
		self.textheight = (self.dialogbox.xy[1] + self.dialogbox.wh[1]) - (self.textmargin * 2)
		self.textsize 	= (self.textwidth, self.textheight)

		# Line counting variables
		self.currentStart = 0
		self.currentEnd = 0

		# Variable lines
		self.allLines = []
		self.currentLine = ""
		self.currentLines = []

		# Variable commands
		self.variables = []
		self.names = {}
		self.nameColor = {}

		# Boolean variables
		self.hide = False

		# Standard background image
		self.background = scLoadImage(self.folder + "assets/gui/backgroundplay.jpg", (WIDTH, HEIGHT))

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
				var = var.replace("name", "")
				var = var.replace(" ", "")

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
		# print(self.currentLine)

		# If this is a replica
		if self.currentLine[0] == "\"" or self.currentLine[0] == "\'":
			self.currentLine = removeChar(self.currentLine)
			self.setLine()
		# If command
		else:
			pass

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

			if self.hide == False:
				# Left mouse button
				if e.button == 1:
					self.nextLine()
				
				# Move the mouse wheel forward
				if e.button == 4:
					self.prevLine()

				# Move the mouse wheel back
				if e.button == 5:
					self.nextLine()

			# Right mouse button
			if e.button == 3:
				if self.hide == True: self.hide = False
				elif self.hide == False: self.hide = True

	# Rendering objects
	def draw(self):
		# Rendering background
		self.screen.blit(self.background, (0, 0))

		if self.hide == False:
			# Rendering dialogbox
			self.dialogbox.draw(self.screen)
			# Rendering text
			self.outLine(self.screen)

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
		x, y = self.textmargin, HEIGHT - (HEIGHT / 4) + self.textmargin
		for line in self.currentLines:
			screen.blit(line, (x, y))
			y += self.lineheight
