# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *
from templates import *

# Class option
class Screen:
	def __init__(self, window, data, options):
		# Window, lines and options variables
		self.window  = window
		self.lines 	 = data
		self.options = options

		# Config variables
		self.config = {}

		# Start screen and current line variables
		self.startScreen = ""
		self.currentLine = ""

		# Line counters variables
		self.currentStart = 0
		self.currentEnd = len(data)

		# Data processing
		self.lineProcessing()

	# Go to the next line
	def nextLine(self):
		self.currentStart += 1
		if self.currentStart >= self.currentEnd: return
		self.lineProcessing()

	# Initial parsing of the line
	def parsingLine(self, line):
		define = re.split(r"(^\w+)", line)
		define = [x for x in define if x != '']
		command, value = "", ""
		if len(define) >= 2:
			command, value = define[0], define[1]
		else: command = define[0]
		return command, value


	# Processing the current line
	def lineProcessing(self):
		self.currentLine = self.lines[self.currentStart]
		if commonCommands(self.currentLine) == False: return self.nextLine()

		# Initial parsing of the line
		command, value = self.parsingLine(self.currentLine)

		# Getting screens
		if command == "screens":
			screens = re.findall(r"\w+", value)
			for screen in screens:
				self.config[screen] = {}
				self.config[screen]["display"] = True
				self.config[screen]["subdisplay"] = False

		# Start screen
		elif command == "init":
			self.startScreen = value.replace(" ", "")

		# Processing screens
		elif command == "screen":
			value = re.sub(r"( )|(:)", "", value)
			if value in self.config:
				start = self.lines.index("screen " + value + ":")
				end = self.lines.index("end " + value)
				lines = self.lines[start:end]
				self.processingScreen(value, lines)
				self.currentStart = end

		# Processing subscreens
		elif command == "subscreen":
			value = re.sub(r"( )|(:)", "", value)
			start = self.lines.index("subscreen " + value + ":")
			end = self.lines.index("end " + value)
			lines = self.lines[start:end]
			self.processingSubscreen(value, lines)
			self.currentStart = end

		self.nextLine()

	# Processing screen
	def processingScreen(self, screen, lines):
		# Optimizable commands
		statics = ["id", "type", "background"]
		
		# Stock position
		elemStart = len(lines)
		actStart = len(lines)

		# Initial positions
		if "elements:" in lines:
			elemStart = lines.index("elements:")
		if "actions:" in lines:
			actStart = lines.index("actions:")

		# Lists elements and actions
		self.elements = lines[elemStart:actStart]
		self.actions  = lines[actStart:len(lines)]

		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = self.parsingLine(line)

			# As an example of some optimization
			if command in statics:
				if command == statics[statics.index(command)]:
					value = value.replace(" ", "")
					self.config[screen][statics[statics.index(command)]] = value

			# Initializing subscreens
			elif command == "subscreens":
				self.config[screen]["subscreens"] = {}
				subscreens = re.findall(r"\w+", value)
				for sub in subscreens:
					self.config[screen]["subscreens"][sub] = {}
					self.config[screen]["subscreens"][sub]["parent"] = screen
					self.config[screen]["subscreens"][sub]["display"] = True

			# Adding interface elements
			elif command == "elements":
				self.config[screen]["elements"] = {}
				self.config[screen]["elements"]["links"] = []
				self.config[screen]["elements"]["buttons"] = []
				self.config[screen]["elements"]["surfaces"] = []
				self.config[screen]["elements"]["inscriptions"] = []
				self.processingElements(screen, self.elements)

			# Handling element actions
			elif command == "actions":
				self.config[screen]["actions"] = {}
				self.config[screen]["actions"]["links"] = []
				self.processingActions(screen, self.actions)

	# Processing elements
	def processingElements(self, screen, lines):
		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = self.parsingLine(line)

			# Adding link
			if command == "link":
				# Creating and adding link
				link = self.createLink(value)
				self.config[screen]["elements"]["links"].append(link)

			# Adding surface
			elif command == "surface":
				# Creating and adding surface
				surface = self.createSurface(value)
				self.config[screen]["elements"]["surfaces"].append(surface)

			# Adding inscription
			elif command == "inscription":
				# Creating and adding inscription
				inscription = self.createInscription(value)
				self.config[screen]["elements"]["inscriptions"].append(inscription)


	# Processing actions
	def processingActions(self, screen, lines):
		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = self.parsingLine(line)

			# Assigning events to link
			if command == "link":
				# Event assignment
				obj = self.actionLink(value)
				# Adding event parameters
				self.config[screen]["actions"]["links"].append(obj)

	# Prcessing subscreen
	def processingSubscreen(self, subscreen, lines):
		# Optimizable commands
		statics = ["id", "type", "background"]
		# Main screen variable
		screen = ""
		
		# Stock position
		elemStart = len(lines)
		actStart = len(lines)

		# Initial positions
		if "elements:" in lines:
			elemStart = lines.index("elements:")
		if "actions:" in lines:
			actStart = lines.index("actions:")

		# Lists elements and actions
		self.elements = lines[elemStart:actStart]
		self.actions  = lines[actStart:len(lines)]

		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = self.parsingLine(line)

			# Getting and check main screen
			screen = getMainScreen(subscreen, self.config)
			if screen == None: return

			# As an example of some optimization
			if command in statics:
				if command == statics[statics.index(command)]:
					value = value.replace(" ", "")
					self.config[screen]["subscreens"][subscreen][statics[statics.index(command)]] = value

			# Adding interface elements
			elif command == "elements":
				self.config[screen]["subscreens"][subscreen]["elements"] = {}
				self.config[screen]["subscreens"][subscreen]["elements"]["links"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["buttons"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["surfaces"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["inscriptions"] = []
				self.processingSubElements(screen, subscreen, self.elements)

			# Handling element actions
			elif command == "actions":
				self.config[screen]["subscreens"][subscreen]["actions"] = {}
				self.config[screen]["subscreens"][subscreen]["actions"]["links"] = []
				self.processingSubActions(screen, subscreen, self.actions)

	# Processing elements for subscreen
	def processingSubElements(self, screen, subscreen, lines):
		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = self.parsingLine(line)

			# Adding link
			if command == "link":
				# Creating and adding link
				link = self.createLink(value)
				self.config[screen]["subscreens"][subscreen]["elements"]["links"].append(link)

			# Adding surface
			elif command == "surface":
				# Creating and adding surface
				surface = self.createSurface(value)
				self.config[screen]["subscreens"][subscreen]["elements"]["surfaces"].append(surface)

			# Adding inscription
			elif command == "inscription":
				# Creating and adding inscription
				inscription = self.createInscription(value)
				self.config[screen]["subscreens"][subscreen]["elements"]["inscriptions"].append(inscription)

	# Processing actions for subscreen
	def processingSubActions(self, screen, subscreen, lines):
		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = self.parsingLine(line)

			# Assigning events to link
			if command == "link":
				# Event assignment
				obj = self.actionLink(value)
				# Adding event parameters
				self.config[screen]["subscreens"][subscreen]["actions"]["links"].append(obj)

	# Passing data to the main class
	def getConfig(self):
		return self.config

	# Create link
	def createLink(self, value):
		# Getting data to add
		name = re.findall(r"\w+", value)[0]
		val = removeChar(re.findall(r"\".*?\"", value)[0])
		xy = defineCoord(re.findall(r"(\(.*?\))", value)[0], self.options["size"])

		# Creating link
		link = Link(name, val, xy, self.options["linkColor"], self.options["linkAim"], self.options["linkSelected"], self.options["linkSize"], self.options["systemFont"])
		return link

	# Create surface
	def createSurface(self, value):
		# Getting data to add
		result = re.findall(r"\w+", value)
		name, alpha = result[0], int(result[1])
		result = re.findall(r"(\(.*?\))", value)
		color = defineColor(result[0])
		xy, wh = defineCoord(result[1], self.options["size"]), defineCoord(result[2], self.options["size"])

		# Creating surface
		surface = Surface(name, alpha, color, xy, wh)
		return surface

	# Create inscription
	def createInscription(self, value):
		# Getting data to add
		name = re.findall(r"\w+", value)[0]
		val = removeChar(re.findall(r"\".*?\"", value)[0])
		xy = defineCoord(re.findall(r"(\(.*?\))", value)[0], self.options["size"])

		# Creating inscription
		inscription = Inscription(name, val, xy, self.options["inscriptionColor"], self.options["inscriptionSize"], self.options["systemFont"])
		return inscription

	# Action link
	def actionLink(self, value):
		# Getting data to add
		parse = re.findall(r"\w+", value)
		name = parse[0]
		tpe, button = "", ""
		event, rtrn = "", ""

		# Calling up the screen
		if parse[1] == "call" or parse[1] == "hide":
			tpe = 1025 # MOUSEBUTTONDOWN
			button = 1 # Left mouse button
			event = parse[1] # Event
			rtrn = parse[2] # Return value

		# Composing an event object
		obj = {
			"name": name,
			"type": tpe,
			"button": button,
			"event": event,
			"return": rtrn
		}

		return obj