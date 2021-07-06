# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *

# Class option
class Screen:
	def __init__(self, window, data):
		# Window, data and dictionary configuration
		self.window = window
		self.data 	= data
		self.config = {}

		# Current screen
		self.currentScreen = ""

		# Data processing
		self.dataProcessing()

	# Data processing
	def dataProcessing(self):
		for line in self.data:
			if commonCommands(line) == False: continue

			define = re.split(r"^([^ ]+)", line)
			define = [x for x in define if x != '']
			# Uh? -1? Why? Why -1?
			command, value = define[0], define[-1]

			# Getting screens
			if command == "screens":
				screens = re.findall(r"\w+", value.replace(" ", ""))
				for screen in screens:
					self.config[screen] = {}
					self.config[screen]["state"] = False

			# Getting script configuration
			elif command == "screen":
				pass

	# Processing screen configurations
	def processingScreen(self, screen):
		pass

	# Passing data to the main class
	def getConfig(self):
		return self.config
