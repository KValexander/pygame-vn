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
		self.lines 	 = data
		self.options = options
		self.screen  = screen
		self.config  = {}

		# Booleand variables
		self.hide = False
		self.back = False

		# Numeric vairables
		self.currentStart = 0
		self.currentEnd = len(self.data)

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
		if commonCommands(self.currentLine) == False: return self.nextLine()
		
		

	# Passing data to the main class
	def getConfig(self):
		return self.config