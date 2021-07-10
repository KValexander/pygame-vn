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

		# Start screen, play screen and current line variables
		self.currentLine = ""

		# Line counters variables
		self.currentStart = 0
		self.currentEnd   = len(data)

		# Data processing
		self.lineProcessing()

	# Go to the next line
	def nextLine(self):
		self.currentStart += 1
		if self.currentStart >= self.currentEnd: return
		self.lineProcessing()

	# Processing the current line
	def lineProcessing(self):
		self.currentLine = self.lines[self.currentStart]
		if commonCommands(self.currentLine) == False: return self.nextLine()

		# Initial parsing of the line
		command, value = parsingLine(self.currentLine)

		# Getting screens
		if command == "screens":
			screens = re.findall(r"\w+", value)
			for screen in screens:
				self.config[screen] = {}
				self.config[screen]["display"] = True
				self.config[screen]["subdisplay"] = False

		# Start screen
		elif command == "init":
			self.config["startScreen"] = value.replace(" ", "")

		# Play screen
		elif command == "playinit":
			self.config["playScreen"] = value.replace(" ", "")

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
		statics = ["id", "type", "background", "startsubscreen"]
		
		# Stock position
		elemStart = len(lines)
		actStart = len(lines)
		playStart = len(lines)

		# Initial positions
		if "elements:" in lines:
			elemStart = lines.index("elements:")
		if "actions:" in lines:
			actStart = lines.index("actions:")
		if "play:" in lines:
			playStart = lines.index("play:")

		# Lists elements and actions
		self.elements = lines[elemStart:actStart]
		self.actions  = lines[actStart:playStart]
		self.play 	  = lines[playStart:len(lines)]

		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = parsingLine(line)

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
				self.config[screen]["elements"]["icons"] = []
				self.config[screen]["elements"]["links"] = []
				self.config[screen]["elements"]["texts"] = []
				self.config[screen]["elements"]["buttons"] = []
				self.config[screen]["elements"]["textures"] = []
				self.config[screen]["elements"]["surfaces"] = []
				self.config[screen]["elements"]["inscriptions"] = []
				self.processingElements(screen, self.elements)

			# Handling element actions
			elif command == "actions":
				self.config[screen]["actions"] = {}
				self.config[screen]["actions"]["mouse"] = []
				self.config[screen]["actions"]["icons"] = []
				self.config[screen]["actions"]["links"] = []
				self.processingActions(screen, self.actions)

			# Play screen only
			elif command == "play" and screen == self.config["playScreen"]:
				self.config[screen]["play"] = {}
				self.config[screen]["play"]["condition"] = {}
				self.config[screen]["play"]["text"] = {}
				self.config[screen]["play"]["events"] = []
				self.processingPlay(screen, self.play)

	# Processing elements
	def processingElements(self, screen, lines):
		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = parsingLine(line)

			# Adding icon
			if command == "icon":
				# Creating and adding icon
				link = self.createIcon(value)
				self.config[screen]["elements"]["icons"].append(link)

			# Adding link
			if command == "link":
				# Creating and adding link
				link = self.createLink(value)
				self.config[screen]["elements"]["links"].append(link)

			# Adding text
			if command == "text":
				# Creating and adding text
				text = self.createText(value)
				self.config[screen]["elements"]["texts"].append(text)

			# Adding texture
			if command == "texture":
				# Creating and adding texture
				texture = self.createTexture(value)
				self.config[screen]["elements"]["textures"].append(texture)

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
			command, value = parsingLine(line)

			# Assigning events to mouse
			if command == "mouse":
				# Event assignment
				obj = self.actionMouse(value)
				# Adding event parameters
				self.config[screen]["actions"]["mouse"].append(obj)

			# Assigning events to icon
			elif command == "icon":
				# Event assignment
				obj = self.actionIcon(value)
				# Adding event parameters
				self.config[screen]["actions"]["icons"].append(obj)

			# Assigning events to link
			elif command == "link":
				# Event assignment
				obj = self.actionLink(value)
				# Adding event parameters
				self.config[screen]["actions"]["links"].append(obj)

	# Processing play
	def processingPlay(self, screen, lines):
		# Stock position
		condStart = len(lines)
		textStart = len(lines)
		evenStart  = len(lines)

		# Initial positions
		if "condition:" in lines:
			condStart = lines.index("condition:")
		if "text:" in lines:
			textStart = lines.index("text:")
		if "events:" in lines:
			evenStart = lines.index("events:")

		# Lists elements and actions
		self.condition 	= lines[condStart:textStart]
		self.text  		= lines[textStart:evenStart]
		self.events 	= lines[evenStart:len(lines)]

		# Handling condition
		for line in self.condition:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = parsingLine(line)
			value = value.replace(" ", "")

			# Text color
			if command == "textcolor":
				self.config[screen]["play"]["condition"]["textColor"] = defineColor(value)
			# Background color
			elif command == "backgroundcolor":
				self.config[screen]["play"]["condition"]["backgroundColor"] = defineColor(value)
			# Indentation
			elif command == "indentation":
				self.config[screen]["play"]["condition"]["indentation"] = int(value)
			# Width
			elif command == "width":
				self.config[screen]["play"]["condition"]["width"] = defineOneSize(value, self.options["size"][0])
			# Height
			elif command == "height":
				self.config[screen]["play"]["condition"]["height"] = defineOneSize(value, self.options["size"][1])

		# Handling text
		for line in self.text:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = parsingLine(line)
			value = value.replace(" ", "")

			# Start coordinate
			if command == "startcoord":
				self.config[screen]["play"]["text"]["startCoord"] = defineSize(value, self.options["size"])
			# Width
			elif command == "width":
				self.config[screen]["play"]["text"]["width"] = defineOneSize(value, self.options["size"][0])
			# Size
			elif command == "size":
				self.config[screen]["play"]["text"]["size"] = int(value)
			# Color
			elif command == "color":
				self.config[screen]["play"]["text"]["color"] = defineColor(value)
			# Line height
			elif command == "lineheight":
				self.config[screen]["play"]["text"]["lineHeight"] = int(value)

		# Handling events
		for line in self.events:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = parsingLine(line)

			# Mouse handling
			if command == "mouse":
				# Event assignment
				obj = self.actionMouse(value)
				# Adding event parameters
				self.config[screen]["play"]["events"].append(obj)

	# Prcessing subscreen
	def processingSubscreen(self, subscreen, lines):
		# Optimizable commands
		statics = ["id", "type", "background", "calltype", "eventmainlock"]
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
			command, value = parsingLine(line)

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
				self.config[screen]["subscreens"][subscreen]["elements"]["icons"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["links"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["texts"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["buttons"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["textures"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["surfaces"] = []
				self.config[screen]["subscreens"][subscreen]["elements"]["inscriptions"] = []
				self.processingSubElements(screen, subscreen, self.elements)

			# Handling element actions
			elif command == "actions":
				self.config[screen]["subscreens"][subscreen]["actions"] = {}
				self.config[screen]["subscreens"][subscreen]["actions"]["mouse"] = []
				self.config[screen]["subscreens"][subscreen]["actions"]["icons"] = []
				self.config[screen]["subscreens"][subscreen]["actions"]["links"] = []
				self.processingSubActions(screen, subscreen, self.actions)

	# Processing elements for subscreen
	def processingSubElements(self, screen, subscreen, lines):
		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = parsingLine(line)

			# Adding icon
			if command == "icon":
				# Creating and adding icon
				link = self.createIcon(value)
				self.config[screen]["subscreens"][subscreen]["elements"]["icons"].append(link)

			# Adding link
			if command == "link":
				# Creating and adding link
				link = self.createLink(value)
				self.config[screen]["subscreens"][subscreen]["elements"]["links"].append(link)

			# Adding text
			if command == "text":
				# Creating and adding text
				text = self.createText(value)
				self.config[screen]["subscreens"][subscreen]["elements"]["texts"].append(text)

			# Adding texture
			if command == "texture":
				# Creating and adding texture
				texture = self.createTexture(value)
				self.config[screen]["subscreens"][subscreen]["elements"]["textures"].append(texture)

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
			command, value = parsingLine(line)

			# Assigning events to mouse
			if command == "mouse":
				# Event assignment
				obj = self.actionMouse(value)
				# Adding event parameters
				self.config[screen]["subscreens"][subscreen]["actions"]["mouse"].append(obj)

			# Assigning events to icon
			elif command == "icon":
				# Event assignment
				obj = self.actionIcon(value)
				# Adding event parameters
				self.config[screen]["subscreens"][subscreen]["actions"]["icons"].append(obj)

			# Assigning events to link
			elif command == "link":
				# Event assignment
				obj = self.actionLink(value)
				# Adding event parameters
				self.config[screen]["subscreens"][subscreen]["actions"]["links"].append(obj)

	# Passing data to the main class
	def getConfig(self):
		return self.config

	# Create icon
	def createIcon(self, value):
		# Getting data to add
		name = re.findall(r"\w+", value)[0]
		src = removeChar(re.findall(r"\".*?\"", value)[0])
		parse = re.findall(r"(\(.*?\))", value)
		xy, wh = defineSize(parse[0], self.options["size"]), None
		if len(parse) >= 2:
			wh = fetchSize(parse[1])

		# Create icon
		icon = Icon(name, src, xy, wh, self.options["pathToScreen"])
		return icon

	# Create link
	def createLink(self, value):
		# Getting data to add
		name = re.findall(r"\w+", value)[0]
		val = removeChar(re.findall(r"\".*?\"", value)[0])
		xy = defineSize(re.findall(r"(\(.*?\))", value)[0], self.options["size"])

		# Creating link
		link = Link(name, val, xy, self.options["linkColor"], self.options["linkAim"], self.options["linkSelected"], self.options["linkSize"], self.options["usedFont"], self.options["typeFont"])
		return link

	# Create text
	def createText(self, value):
		# Getting data to add
		name = re.findall(r"\w+", value)[0]
		val = removeChar(re.findall(r"\".*?\"", value)[0])
		xy = defineSize(re.findall(r"(\(.*?\))", value)[0], self.options["size"])
		width = defineOneSize(re.findall(r"(\(.*?\))", value)[1], self.options["size"][0])

		# Creating text
		text = Text(name, val, xy, width, self.options["textColor"], self.options["textSize"], self.options["textLineHeight"], self.options["usedFont"], self.options["typeFont"])
		return text

	# Create texture
	def createTexture(self, value):
		# Getting data to add
		name = re.findall(r"\w+", value)[0]
		src = removeChar(re.findall(r"\".*?\"", value)[0])
		parse = re.findall(r"(\(.*?\))", value)
		xy, wh = defineSize(parse[0], self.options["size"]), defineSize(parse[1], self.options["size"])

		# Create texture
		texture = Texture(name, src, xy, wh, self.options["pathToScreen"])
		return texture

	# Create surface
	def createSurface(self, value):
		# Getting data to add
		parse = re.findall(r"\w+", value)
		name, alpha = parse[0], int(parse[1])
		parse = re.findall(r"(\(.*?\))", value)
		color = defineColor(parse[0])
		xy, wh = defineSize(parse[1], self.options["size"]), defineSize(parse[2], self.options["size"])

		# Creating surface
		surface = Surface(name, alpha, color, xy, wh)
		return surface

	# Create inscription
	def createInscription(self, value):
		# Getting data to add
		name = re.findall(r"\w+", value)[0]
		val = removeChar(re.findall(r"\".*?\"", value)[0])
		xy = defineSize(re.findall(r"(\(.*?\))", value)[0], self.options["size"])

		# Creating inscription
		inscription = Inscription(name, val, xy, self.options["inscriptionColor"], self.options["inscriptionSize"], self.options["usedFont"], self.options["typeFont"])
		return inscription

	# Action mouse
	def actionMouse(self, value):
		# Getting data to add
		parse = re.findall(r"\w+", value)
		tpe, button = None, None
		event, rtrn = None, None

		if parse[0] == "leftclick": button = 1
		elif parse[0] == "middleclick": button = 2
		elif parse[0] == "rightclick": button = 3
		elif parse[0] == "wheelup": button = 4
		elif parse[0] == "wheelbottom": button = 5

		# Calling and hide up the screen
		if parse[1] == "call" or parse[1] == "hide":
			tpe = 1025 #MOUSEBUTTONDOWN
			event = parse[1] # Event
			rtrn = parse[2] # Return value

		# Closing the current screen or Closing the window
		elif parse[1] == "close" or parse[1] == "end" or parse[1] == "start":
			tpe = 1025
			event = parse[1]
			rtrn = parse[1]

		# Otherwise
		else:
			tpe = 1025
			event = parse[1]
			rtrn = parse[1]

		# Composing an event object
		obj = {
			"type": tpe,
			"button": button,
			"event": event,
			"return": rtrn
		}

		return obj

	# Action icon
	def actionIcon(self, value):
		# Getting data to add
		parse = re.findall(r"\w+", value)
		name, src = parse[0], None
		tpe, button = None, None
		event, rtrn = None, None

		# Hovering over an icon
		if parse[1] == "hover":
			src = removeChar(re.findall(r"\".*?\"", value)[0]) # Path to image hover
			tpe = 1024 #MOUSEMOTION
			event = parse[1] # Event

		# Calling and hide up the screen
		elif parse[1] == "call" or parse[1] == "hide":
			tpe = 1025 # MOUSEBUTTONDOWN
			button = 1 # Left mouse button
			event = parse[1] # Event
			rtrn = parse[2] # Return value

		# Closing the current screen or Closing the window
		elif parse[1] == "close" or parse[1] == "end" or parse[1] == "start":
			tpe = 1025
			button = 1
			event = parse[1]
			rtrn = parse[1]

		# Composing an event object
		obj = {
			"name": name,
			"src": src,
			"type": tpe,
			"button": button,
			"event": event,
			"return": rtrn
		}

		return obj

	# Action link
	def actionLink(self, value):
		# Getting data to add
		parse = re.findall(r"\w+", value)
		name = parse[0]
		tpe, button = None, None
		event, rtrn = None, None

		# Calling and hide up the screen
		if parse[1] == "call" or parse[1] == "hide":
			tpe = 1025 # MOUSEBUTTONDOWN
			button = 1 # Left mouse button
			event = parse[1] # Event
			rtrn = parse[2] # Return value

		# Closing the current screen or Closing the window
		elif parse[1] == "close" or parse[1] == "end" or parse[1] == "start":
			tpe = 1025
			button = 1
			event = parse[1]
			rtrn = parse[1]

		# Composing an event object
		obj = {
			"name": name,
			"type": tpe,
			"button": button,
			"event": event,
			"return": rtrn
		}

		return obj