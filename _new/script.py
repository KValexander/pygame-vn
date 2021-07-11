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
	def __init__(self, window, data, options, screen, main):
		# Window, lines, options, screen, main and config variables
		self.window  = window
		self.data 	 = data
		self.options = options
		self.screen  = screen
		self.main 	 = main

		# Config variables
		self.config  = {
			# Font
			"font": "",
			# Lines
			"lines": {
				"start": 0,
				"end": 0,
				"name": "",
				"line": "",
				"lines": []
			},
			# Name key
			"namekey": "",
			# Background
			"background": scLoadImage(self.options["pathToBackgroundStock"], self.options["size"]),
			# Variables
			"variables": {
				"counters": {},
				"names": {},
				"characters": {},
			},
			# Rendering
			"render": {
				"characters": {},
			},
			# Conditions
			"conditions": {},
			# Boolean
			"bool": {
				"hide": False,
				"back": False,
				"start": False,
				"choice": False,
				"nameshow": False,
			},
		}

		# Set font
		self.setFont("text")

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
		self.config["lines"]["end"] = len(self.lines) - 1

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
			elif command == "character":
				# Getting data to add
				name = re.findall(r"\w+", value)[0]
				parse = removeChar(re.findall(r"\(.*\(.*?\)\)", value)[0])
				src = removeChar(re.findall(r"\".*?\"", parse)[0])
				coord = defineSize(re.findall(r"\(.*?\)", parse)[0], self.options["size"])

				# Adding data
				self.config["variables"]["characters"][name] = { "src": src, "coord": coord }

			# Variable handling with type "count"
			elif command == "count":
				# Getting data to add
				parse = re.findall(r"\w+", value)
				name, count = parse[0], int(parse[1])

				# Adding data
				self.config["variables"]["counters"][name] = count

	# Next line
	def nextLine(self):
		self.config["lines"]["start"] += 1
		self.config["bool"]["back"] = False

		# If all the lines are finished
		if self.config["lines"]["start"] > self.config["lines"]["end"]:
			return self.main.refreshScreen(self.main.startScreen)

		self.lineProcessing()

	# Prev line
	def prevLine(self):
		self.config["lines"]["start"] -= 1
		self.config["bool"]["back"] = True

		# If there is no current line
		if self.config["lines"]["start"] <= 0:
			self.config["bool"]["back"] = False
			self.config["lines"]["start"] = 0

		self.lineProcessing()

	# Processing the current line
	def lineProcessing(self):
		# Current line
		self.config["lines"]["line"] = self.lines[self.config["lines"]["start"]]
		
		# If current line = return
		if self.config["lines"]["line"] == "return":
			return self.main.refreshScreen(self.main.startScreen)

		# Getting rid of comments
		if commonCommands(self.config["lines"]["line"]) == False:
			if self.config["bool"]["back"]: return self.prevLine()
			else: return self.nextLine()

		# Line output with no name
		if re.search(r"(^\".*?\"$)", self.config["lines"]["line"]):
			self.setReplica()
		# Line with commands
		else: self.commandProcessing()

	# Processing commands within script lines
	def commandProcessing(self):
		# Initial parsing of the line
		command, value = parsingLine(self.config["lines"]["line"])

		# Check name
		if command in self.config["variables"]["names"]:
			self.config["namekey"] = command
			self.config["bool"]["nameshow"] = True
			self.setNameOnLine()

			self.config["lines"]["line"] = removeChar(value.replace(" ", "", 1))
			return self.setTextOnLine()

		# Background
		elif command == "background":
			self.setBackground(value)

		# Show characters
		elif command == "show":
			self.showCharacters(value)

		# Hide characters
		elif command == "hide":
			self.hideCharacter(value)

		# Going to label
		elif command == "go":
			self.setLabel(value)

		# Label
		elif command == "label":
			self.config["bool"]["back"] = False

		if self.config["bool"]["back"]: self.prevLine()
		else: self.nextLine()

	# Handling events
	def events(self, e):
		if self.config["bool"]["start"] == False: self.config["bool"]["start"] = True
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

	# Rendering background
	def background(self, window):
		# Rendering background
		if self.config["background"] != None:
			drawImage(self.window, self.config["background"], (0,0))

		# Rendering characters
		if len(self.config["render"]["characters"]) != 0:
			for character in self.config["render"]["characters"]:
				if self.config["render"]["characters"][character]["state"]:
					drawImage(window, self.config["render"]["characters"][character]["image"], self.config["render"]["characters"][character]["coord"])

	# Output text on window
	def outTextOnWindow(self, window):
		# Rendering lines
		x, y = self.screen["text"]["startCoord"]
		for line in self.config["lines"]["lines"]:
			window.blit(line, (x, y))
			y += self.screen["text"]["lineHeight"]

		# Rendering name
		if self.config["bool"]["nameshow"]:
			window.blit(self.config["lines"]["name"], self.screen["name"]["startCoord"])

	# Passing data to the main class
	def getConfig(self):
		return self.config


	# Set font
	def setFont(self, case):
		size = self.screen[case]["size"]
		if self.options["typeFont"] == "system":
			self.config["font"] = pygame.font.SysFont(self.options["usedFont"], size)
		elif self.options["typeFont"] == "own":
			if os.path.exists(self.options["usedFont"]):
				self.config["font"] = pygame.font.Font(self.options["usedFont"], size)
			else: self.config["font"] = pygame.font.SysFont("calibri", size)
		else: self.config["font"] = pygame.font.SysFont("calibri", size)

	# Set replica
	def setReplica(self):
		self.config["lines"]["line"] = removeChar(self.config["lines"]["line"])
		# Replacing part of a string with variables
		if re.search(r"{.}", self.config["lines"]["line"]):
			for count in re.finditer(r"{.}", self.config["lines"]["line"]):
				counter = removeChar(count[0])
				if counter in self.config["variables"]["counters"]:
					self.config["lines"]["line"] = re.sub(r"{"+counter+"}", str(self.config["variables"]["counters"][counter]), self.config["lines"]["line"])
		# Set text on line
		self.config["bool"]["nameshow"] = False
		self.setTextOnLine()

	# Set name on line
	def setNameOnLine(self):
		self.setFont("name")
		self.config["lines"]["name"] = self.config["font"].render(self.config["variables"]["names"][self.config["namekey"]]["value"], True, self.config["variables"]["names"][self.config["namekey"]]["color"])

	# Set text to line
	def setTextOnLine(self):
		self.setFont("text")
		self.config["lines"]["lines"].clear()
		for value in processingLine(self.config["lines"]["line"], self.screen["text"]["width"], self.config["font"]):
			line = self.config["font"].render(str(value), True, self.screen["text"]["color"])
			self.config["lines"]["lines"].append(line)

	# Set background
	def setBackground(self, value):
		value = removeChar(value.replace(" ", ""))
		src = self.options["pathToBackground"] + value
		if os.path.exists(src) == False:
			src = self.options["pathToBackgroundStock"]
		self.config["background"] = scLoadImage(src, self.options["size"])

	# Handling show characters
	def showCharacters(self, value):
		# Parsing value
		value = re.findall(r"\w+", value)

		# If the character has already been show
		if value[0] in self.config["render"]["characters"]:
			state = True
			if self.config["bool"]["back"]: state = False
			self.config["render"]["characters"][value[0]]["state"] = state

			# If there is positioning
			if len(value) >= 2:
				self.characterPos(value)
		else:
			# Getting src and coord for image
			if value[0] in self.config["variables"]["characters"]:
				coord = self.config["variables"]["characters"][value[0]]["coord"]
				src = self.options["pathToCharacter"] + value[0]
				if os.path.exists(src) == False:
					src = self.options["pathToCharacterStock"]
			else:
				coord = (0, 0)
				src = self.options["pathToCharacterStock"]

			# Adding data
			self.config["render"]["characters"][value[0]] = {
				"image": loadImage(src),
				"coord": coord,
				"state": True
			}

			# If there is positioning
			if len(value) >= 2:
				self.characterPos(value)

	# Character positioning
	def characterPos(self, value):
		rect = self.config["render"]["characters"][value[0]]["image"].get_rect()
		if value[1] == "left": coord = (self.options["size"][0] * 0.15 - rect.width / 2, self.options["size"][1] - rect.height)
		elif value[1] == "center": coord = (self.options["size"][0] * 0.5 - rect.width / 2, self.options["size"][1] - rect.height)
		elif value[1] == "right": coord = (self.options["size"][0] * 0.85 - rect.width / 2, self.options["size"][1] - rect.height)
		self.config["render"]["characters"][value[0]]["coord"] = coord

	# Handling hide characters
	def hideCharacter(self, value):
		character = value.replace(" ", "")
		# Hiding one specific character
		if character in self.config["render"]["characters"]:
			state = False
			if self.config["bool"]["back"]: state = True
			self.config["render"]["characters"][character]["state"] = state
		# Hiding all characters
		elif character == "characters":
			for char in self.config["render"]["characters"]:
				self.config["render"]["characters"][char]["state"] = False

	# Set label
	def setLabel(self, value):
		label = self.lines.index("label " + value.replace(" ", "") + ":")
		self.config["lines"]["start"] = label
