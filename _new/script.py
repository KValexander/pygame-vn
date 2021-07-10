# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *

# Class option
class Script:
	def __init__(self, window, data, options, screen):
		# Window, lines, options, screen and config variables
		self.window  = window
		self.data 	 = data
		self.options = options
		self.screen  = screen

		# Font variable
		if self.options["typeFont"] == "system":
			self.font = pygame.font.SysFont(self.options["usedFont"], self.screen["text"]["size"])
		elif self.options["typeFont"] == "own":
			if os.path.exists(self.options["usedFont"]):
				self.font = pygame.font.Font(self.options["usedFont"], self.screen["text"]["size"])
			else: self.font = pygame.font.SysFont("calibri", self.screen["text"]["size"])
		else: self.font = pygame.font.SysFont("calibri", self.screen["text"]["size"])

		# Config variables
		self.config  = {
			"conditions": {},
			"variables": {
				"counters": {},
				"names": {},
				"characters": {},
			},
			"rendering": {
				"characters": {
					"image": "",
					"coord": ()
				},
			},
		}

		# Booleand variables
		self.hide 		= False
		self.back 		= False
		self.start 		= False
		self.choice 	= False
		self.nameshow 	= False

		# Numeric vairables
		self.currentStart = 0
		self.currentEnd = 0

		# Line variables
		self.currentLine = ""
		self.currentLines = []

		# Handling variables
		self.variables = []
		self.lines = []

		# Data processing
		self.dataProcessing()
		# Variables processing
		self.variablesProcessing()
		# Line processing
		self.lineProcessing()

	# Data processing
	def dataProcessing(self):
		linestart = self.data.index("start:")
		self.variables = self.data[0:linestart]
		self.lines = self.data[linestart:len(self.data)]
		self.currentEnd = len(self.lines) - 1

	# Variables processing
	def variablesProcessing(self):
		# Handling lines
		for line in self.variables:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = parsingLine(line)

			# Variable handling with type "name"
			if command == "name":
				# Getting data to add
				name = re.findall(r"\w+", value)[0]
				parse = removeChar(re.findall(r"\(.*\(.*?\)\)", value)[0])
				val = removeChar(re.findall(r"\".*?\"", parse)[0])
				color = defineColor(re.findall(r"\(.*?\)", parse)[0])

				# Adding data
				self.config["variables"]["names"][name] = { "value": val, "color": color }

			# Variable handling with type "character"
			if command == "character":
				# Getting data to add
				name = re.findall(r"\w+", value)[0]
				parse = removeChar(re.findall(r"\(.*\(.*?\)\)", value)[0])
				src = removeChar(re.findall(r"\".*?\"", parse)[0])
				coord = defineSize(re.findall(r"\(.*?\)", parse)[0], self.options["size"])

				# Adding data
				self.config["variables"]["characters"][name] = { "src": src, "coord": coord }

			# Variable handling with type "count"
			if command == "count":
				# Getting data to add
				parse = re.findall(r"\w+", value)
				name, count = parse[0], int(parse[1])

				# Adding data
				self.config["variables"]["counters"][name] = count

	# Next line
	def nextLine(self):
		self.currentStart += 1
		self.back = False
		if self.currentStart >= self.currentEnd:
			self.currentStart = self.currentEnd
			return
		self.lineProcessing()

	# Prev line
	def prevLine(self):
		self.currentStart -= 1
		self.back = True
		if self.currentStart <= 0: self.currentStart = 0
		self.lineProcessing()

	# Processing the current line
	def lineProcessing(self):
		self.currentLine = self.lines[self.currentStart]
		# Getting rid of comments
		if commonCommands(self.currentLine) == False:
			if self.back: return self.prevLine()
			else: return self.nextLine()

		# Line output with no name
		if re.search(r"^\".*?\"$", self.currentLine):
			self.currentLine = removeChar(self.currentLine)
			# Replacing part of a string with variables
			if re.search(r"{.}", self.currentLine):
				for count in re.finditer(r"{.}", self.currentLine):
					counter = removeChar(count[0])
					if counter in self.config["variables"]["counters"]:
						self.currentLine = re.sub(r"{"+counter+"}", str(self.config["variables"]["counters"][counter]), self.currentLine)
			# Set text on line
			self.nameshow = False
			self.setTextOnLine()

		# Line with commands
		else:
			self.nextLine()

	# Set text to line
	def setTextOnLine(self):
		self.currentLines.clear()
		for value in processingLine(self.currentLine, self.screen["text"]["width"], self.font):
			line = self.font.render(str(value), True, self.screen["text"]["color"])
			self.currentLines.append(line)

	# Output text on window
	def outTextOnWindow(self, window):
		x, y = self.screen["text"]["startCoord"]
		for line in self.currentLines:
			window.blit(line, (x, y))
			y += self.screen["text"]["lineHeight"]

	# Handling events
	def events(self, e):
		if self.start == False: self.start = True
		else:
			# Handling events
			for event in self.screen["events"]:
				# Event handling
				if e.type == event["type"]:
					if e.button == event["button"]:
						if event["event"] == "nextline":
							self.nextLine()
						elif event["event"] == "prevline":
							self.prevLine()


	# Rendering objects
	def draw(self, window):
		self.outTextOnWindow(window)

	# Passing data to the main class
	def getConfig(self):
		return self.config