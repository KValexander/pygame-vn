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
			"font": {},
			# Variables
			"variables": {
				"counters": {},
				"booleans": {},
				"names": {},
				"characters": {},
			},
			# Lines
			"lines": {
				"start": 0,
				"end": 0,
				"namekey": "",
				"name": "",
				"line": "",
				"lines": []
			},
			# Background
			"background": {
				"src": self.options["pathToBackgroundStock"],
				"image":scLoadImage(self.options["pathToBackgroundStock"], self.options["size"]),
			},
			# Rendering
			"render": {
				"characters": {},
				"clauses": [],
			},
			# Condition
			"condition": {},
			# Boolean
			"bool": {
				"hide": False,
				"back": False,
				"start": False,
				"choice": False,
				"nameshow": False,
				"output": False,
				"music": False,
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

			# Variable handling with type "boolean"
			elif command == "bool":
				# Getting data to add
				parse = re.findall(r"\w+", value)
				name, state = parse[0], parse[1]

				# Adding data
				self.config["variables"]["booleans"][name] = state

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
		if re.search(r"(^\".*?\"$)|(^\'.*?\'$)", self.config["lines"]["line"]):
			self.setReplica()
		# Line with commands
		else: self.commandProcessing()

	# Processing commands within script lines
	def commandProcessing(self):
		# Initial parsing of the line
		command, value = parsingLine(self.config["lines"]["line"])

		# Check name
		if command in self.config["variables"]["names"]:
			self.config["lines"]["namekey"] = command
			self.setNameOnLine()

			self.config["lines"]["line"] = removeChar(value.replace(" ", "", 1))
			return self.setTextOnLine()

		# Check counters
		elif command in self.config["variables"]["counters"]:
			if value == "++":
				self.config["variables"]["counters"][command] += 1
			elif value == "--":
				self.config["variables"]["counters"][command] -= 1
				
		# Check boolean
		elif command in self.config["variables"]["booleans"]:
			value = value.replace(" ", "")
			if value == "True" or value == "False": self.config["variables"]["booleans"][command] = value

		# Background
		elif command == "background":
			self.setBackground(removeChar(value.replace(" ", "")))

		# Show characters
		elif command == "show":
			self.showCharacters(value)

		# Hide characters
		elif command == "hide":
			self.hideCharacter(value)

		# Condition
		elif command == "condition":
			self.config["bool"]["choice"] = True
			return self.setCondition(value)

		# If else condition
		elif command == "if":
			return self.operatorsHandling()

		# Going to label
		elif command == "go":
			self.setLabel(value)

		# Label
		elif command == "label":
			self.config["bool"]["back"] = False

		if self.config["bool"]["back"]: self.prevLine()
		else: self.nextLine()

	# Handling commands
	def handlingCommands(self, commands):
		# Handling commands
		for command in commands:
			command = command.replace(" ", "", 1)

			# Check text
			if re.search(r"(^\".*?\"$)|(^\'.*?\'$)", command):
				self.config["lines"]["line"] = command
				self.setReplica()
				return False

			parse = re.findall(r"\w+", command)

			# Check name
			if parse[0] in self.config["variables"]["names"]:
				name, value = parsingLine(command)
				self.config["lines"]["namekey"] = name
				self.setNameOnLine()

				self.config["lines"]["line"] = removeChar(value.replace(" ", "", 1))
				self.setTextOnLine()
				return False

			# Check boolean
			elif parse[0] in self.config["variables"]["booleans"]:
				if parse[1] == "True" or parse[1] == "False": 
					self.config["variables"]["booleans"][parse[0]] = parse[1]

			# Check counters
			elif parse[0] in self.config["variables"]["counters"]:
				if command.find("++") != -1:
					self.config["variables"]["counters"][parse[0]] += 1
				elif command.find("--") != -1:
					self.config["variables"]["counters"][parse[0]] -= 1

			# Going to label
			elif parse[0] == "go": self.setLabel(parse[1])

			# Background
			elif parse[0] == "background":
				self.setBackground(parse[1] + "." + parse[2])

			# Show characters
			elif parse[0] == "show":
				val = parse[1]
				if len(parse) >= 3: val = parse[1] + " " + parse[2]
				self.showCharacters(val)

			# Hide characters
			elif parse[0] == "hide":
				self.hideCharacter(parse[1])

			# Continue
			elif parse[0] == "continue": continue
		return True

	# Handling events
	def events(self, e):
		if self.config["bool"]["start"] == False: self.config["bool"]["start"] = True
		elif self.config["bool"]["choice"] == False:
			# Handling mouse events
			for event in self.screen["events"]["mouse"]:
				# Event handling
				if e.type == event["type"]:
					if e.button == event["button"]:
						if event["event"] == "nextline":
							self.nextLine()
						elif event["event"] == "prevline":
							self.prevLine()
			# Handling icons events
			for jicon in self.screen["events"]["icons"]:
				# Getting icon
				ricon = getElementByName(jicon["name"], self.main.currentScreen["elements"]["icons"])
				if ricon == None: return
				# Event handling
				if e.type == jicon["type"]:
					if e.button == jicon["button"]:
						if mouseCollision(ricon.xy, ricon.wh, e.pos):
							if jicon["event"] == "nextline":
								self.nextLine()
							elif jicon["event"] == "prevline":
								self.prevLine()
			# Handling icons events
			for jlink in self.screen["events"]["icons"]:
				# Getting a link
				rlink = getElementByName(jlink["name"], self.main.currentScreen["elements"]["links"])
				if rlink == None: return
				# Event handling
				if e.type == jlink["type"]:
					if e.button == jlink["button"]:
						if mouseCollision(rlink.xy, rlink.twh, e.pos):
							if jlink["event"] == "nextline":
								self.nextLine()
							elif jlink["event"] == "prevline":
								self.prevLine()
		elif self.config["bool"]["choice"]:
			# Condition clause events
			self.eventCondition(e)

	# Condition clause events
	def eventCondition(self, e):
		# Condition clause selection processing
		for clause in self.config["render"]["clauses"]:
			# Handling a click on a condition clause
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					if mouseCollision(clause["xy"], clause["wh"], e.pos):
						self.conditionProcessing(clause["return"])

			# Processing of pointing to a condition clause
			if e.type == pygame.MOUSEMOTION:
				if mouseCollision(clause["xy"], clause["wh"], e.pos):
					clause["hover"] = True
				else: clause["hover"] = False

	# Rendering objects
	def draw(self, window):
		self.outTextOnWindow(window)

	# Rendering background
	def background(self, window):
		# Rendering background
		drawImage(self.window, self.config["background"]["image"], (0,0))

		# Rendering characters
		if len(self.config["render"]["characters"]) != 0:
			for character in self.config["render"]["characters"]:
				if self.config["render"]["characters"][character]["state"]:
					drawImage(window, self.config["render"]["characters"][character]["image"], self.config["render"]["characters"][character]["coord"])

		# Rendering condition
		if self.config["bool"]["choice"]:
			self.drawCondition(window)

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

	# Rendering cluses condition
	def drawCondition(self, window):
		window.blit(self.config["condition"]["surface"], self.config["condition"]["xy"])
		window.blit(self.config["condition"]["text"], self.config["condition"]["txy"])

		for clause in self.config["render"]["clauses"]:
			window.blit(self.config["condition"]["surface"], clause["xy"])
			window.blit(clause["text"], clause["txy"])
			if clause["hover"]:
				pygame.draw.rect(window, self.options["conditionOutlineColor"], (clause["xy"], clause["wh"]), self.options["conditionBorder"])

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
		# Set text on line
		self.config["lines"]["line"] = removeChar(self.config["lines"]["line"])
		self.config["bool"]["nameshow"] = False
		self.setTextOnLine()

	# Replacing Variables with Values
	def replacingLines(self):
		# Replacing part of a string with variables
		if re.search(r"{.}", self.config["lines"]["line"]):
			for count in re.finditer(r"{.}", self.config["lines"]["line"]):
				counter = removeChar(count[0])
				if counter in self.config["variables"]["counters"]:
					self.config["lines"]["line"] = re.sub(r"{"+counter+"}", str(self.config["variables"]["counters"][counter]), self.config["lines"]["line"])

	# Set name on line
	def setNameOnLine(self):
		self.config["bool"]["nameshow"] = True
		self.setFont("name")
		self.config["lines"]["name"] = self.config["font"].render(self.config["variables"]["names"][self.config["lines"]["namekey"]]["value"], True, self.config["variables"]["names"][self.config["lines"]["namekey"]]["color"])

	# Set text to line
	def setTextOnLine(self):
		# Replacing part of a string with variables
		self.replacingLines()
		self.setFont("text")
		self.config["lines"]["lines"].clear()
		for value in processingLine(self.config["lines"]["line"], self.screen["text"]["width"], self.config["font"]):
			line = self.config["font"].render(str(value), True, self.screen["text"]["color"])
			self.config["lines"]["lines"].append(line)

	# Set background
	def setBackground(self, value):
		src = self.options["pathToBackground"] + value
		if os.path.exists(src) == False:
			src = self.options["pathToBackgroundStock"]
		self.config["background"]["src"] = src
		self.config["background"]["image"] = scLoadImage(src, self.options["size"])

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
				src = self.options["pathToCharacter"] + self.config["variables"]["characters"][value[0]]["src"]
				if os.path.exists(src) == False:
					src = self.options["pathToCharacterStock"]
			else:
				coord = (0, 0)
				src = self.options["pathToCharacterStock"]

			# Adding data
			self.config["render"]["characters"][value[0]] = {
				"image": loadImage(src),
				"state": True,
				"coord": coord,
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

	# Condition fulfillment processing
	def conditionProcessing(self, commands):
		commands = commands.split(";")
		self.config["bool"]["back"] = False
		self.config["bool"]["choice"] = False

		# Handling commands
		if self.handlingCommands(commands):
			self.lineProcessing()

	# Set condition
	def setCondition(self, value):
		self.config["condition"].clear()
		self.config["render"]["clauses"].clear()

		# Parsing in the output of a condition
		value = re.findall(r"(\".*?\")|(\'.*?\')", value)[0]
		value = removeChar([x for x in value if x != ''][0])
		self.config["lines"]["line"] = value
		self.setTextOnLine()

		# Receiving all clauses of conditions
		start = self.config["lines"]["start"]
		ends = [x[0] for x in enumerate(self.lines) if x[1] == "end condition"]
		
		# Sorting and getting the closest condition close value
		ends = [x for x in ends if x > start]
		minimum = float("inf")
		for val in ends:
			if abs(val - start) < minimum:
				end = val
				minimum = abs(val - start)

		# Getting a list of conditions
		clauses = self.lines[start:end]
		clauses.pop(0)

		# By the end of the condition
		self.config["lines"]["start"] = end

		# Getting condition data
		size = self.config["font"].size(value)
		text = self.config["font"].render(value, True, self.options["conditionTextColor"])
		wh = (size[0] + self.options["conditionMargin"] * 2, size[1] + self.options["conditionMargin"])
		xy = (self.options["size"][0] / 2 - wh[0] / 2, self.options["size"][1] / 2 - wh[1] - ((len(clauses) - 1) * self.options["conditionIndentation"]))
		txy = (xy[0] + self.options["conditionMargin"], xy[1] + self.options["conditionMargin"] / 2)
		
		surface = pygame.Surface(wh)
		surface.fill(self.options["conditionBackgroundColor"])
		surface.set_alpha(self.options["conditionAlpha"])

		# Adding condition data
		self.config["condition"]["value"] = value
		self.config["condition"]["text"] = text
		self.config["condition"]["wh"] = wh
		self.config["condition"]["xy"] = xy
		self.config["condition"]["txy"] = txy
		self.config["condition"]["surface"] = surface

		x, y = xy
		# Handling clauses
		for claus in clauses:
			y += self.options["conditionIndentation"]
			value, commands = claus.split(":")
			text = self.config["font"].render(value, True, self.options["conditionTextColor"])
			twh = self.config["font"].size(value)
			txy = x + wh[0] / 2 - twh[0] / 2, y + wh[1] / 2 - twh[1] / 2

			self.config["render"]["clauses"].append({
				"xy": (x, y),
				"wh": wh,
				"value": value,
				"text": text,
				"txy": txy,
				"twh": twh,
				"return": commands,
				"hover": False
			})

	# Operator command processing
	def operatorProcessing(self, commands):
		commands = commands.split(";")

		# Handling commands
		if self.handlingCommands(commands):
			if self.config["bool"]["back"]: return self.prevLine()
			else: return self.nextLine()

	# Operators handling
	def operatorsHandling(self):
		start = self.config["lines"]["start"]
		ends = [x[0] for x in enumerate(self.lines) if x[1] == "end if" or x[1] == "endif"]
		
		# Sorting and getting the closest operators close value
		ends = [x for x in ends if x > start]
		minimum = float("inf")
		for val in ends:
			if abs(val - start) < minimum:
				end = val
				minimum = abs(val - start)

		# Getting a list of operators
		operators = self.lines[start:end]

		# Handling operators
		for line in operators:
			operator, value = parsingLine(line)
			value = value.split(":")
			value[0] = value[0].replace(" ", "")

			if operator == "else":
				self.operatorProcessing(value[1])
				break
			elif operator == "if":
				if self.operatorsCheck(value[0]):
					self.operatorProcessing(value[1])
					break
			elif operator == "elif":
				if self.operatorsCheck(value[0]):
					self.operatorProcessing(value[1])
					break
			else: break

	# Checking comparison operators
	def operatorsCheck(self, check):
		# Check boolean variables
		if check in self.config["variables"]["booleans"]:
			if self.config["variables"]["booleans"][check] == "True":
				return True
			else: return False

		# Check counter variables
		arrcond = ["==", "<=", ">=", "<", ">", "!="]
		for i in range(len(arrcond)):
			if check.find(arrcond[i]) != -1:
				cond = check.split(arrcond[i])
				if cond[0] in self.config["variables"]["counters"]: cond[0] = self.config["variables"]["counters"][cond[0]]
				else: cond[0] = int(cond[0])
				if cond[1] in self.config["variables"]["counters"]: cond[1] = self.config["variables"]["counters"][cond[1]]
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

	# Set label
	def setLabel(self, value):
		label = self.lines.index("label " + value.replace(" ", "") + ":")
		self.config["lines"]["start"] = label