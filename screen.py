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
	def __init__(self, window, data):
		# Window and lines variables
		self.window = window
		self.lines = data

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

		# Start screen
		if command == "init":
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
				self.processingActions(screen, self.actions)

	# Processing elements
	def processingElements(self, screen, lines):
		# Handling lines
		for line in lines:
			if commonCommands(line) == False: continue

			# Initial parsing of the line
			command, value = self.parsingLine(line)

			# Adding surface
			if command == "surface":
				result = re.findall(r"\w+", value)
				name, alpha = result[0], result[1]
				result = re.findall(r"(\(.*?\))", value)
				сolor = result[0]
				xy = result[1]
				wh = result[2]

	# Processing actions
	def processingActions(self, screen, actions):
		pass

	# Passing data to the main class
	def getConfig(self):
		print(self.config)
		return self.config
