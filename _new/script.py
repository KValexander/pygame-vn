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

		# Config variables
		self.config  = {
			"variables": {
				"counters": {},
				"names": {
					"value": "",
					"color": ()
				},
				"characters": {
					"src": "",
					"coord": ()
				},
			},
			"rendering": {
				"characters": {
					"image": "",
					"coord": ()
				},
			},
		}

		# Booleand variables
		self.hide 	= False
		self.back 	= False
		self.choice = False

		# Numeric vairables
		self.currentStart = 0
		self.currentEnd = len(self.data)

		# Line variables
		self.currentLine = ""

		# Handling variables
		self.variables = []
		self.lines = []

		# Data processing
		self.dataProcessing()
		# Variables processing
		self.variablesProcessing()

	# Data processing
	def dataProcessing(self):
		linestart = self.data.index("start:")
		self.variables = self.data[0:linestart]
		self.lines = self.data[linestart:self.currentEnd]

	# Variables processing
	def variablesProcessing(self):
		# Handling lines
		for variable in self.variables:
			if commonCommands(variable) == False: return self.nextLine()
			print(variable)

	# Next line
	def nextLine(self):
		self.currentStart += 1
		if self.currentStart >= self.currentEnd: return
		self.lineProcessing()

	# Prev line
	def prevLine(self):
		self.currentStart -= 1
		if self.currentStart <= 0: self.currentStart = 0
		self.lineProcessing()

	# Processing the current line
	def lineProcessing(self):
		self.currentLine = self.lines[self.currentStart]
		if commonCommands(self.currentLine) == False:
			if self.back: return self.prevLine()
			else: return self.nextLine()

	# Handling events
	def events(self, e):
		pass

	# Passing data to the main class
	def getConfig(self):
		return self.config