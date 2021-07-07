# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *

# Class option
class Option:
	def __init__(self, data):
		self.data 	= data
		self.config = {}

		# Data processing
		self.dataProcessing()

	# Data processing
	def dataProcessing(self):
		for line in self.data:
			if commonCommands(line) == False: continue
			line = line.replace(" ", "")
			name, value = line.split("=")

			# Screen resolution
			if line.find("window_size") != -1:
				self.config["size"] = defineResolution(value)

			# The name of the project
			elif line.find("project_name") != -1:
				self.config["projectName"] = removeChar(value)

			# FPS
			elif line.find("fps") != -1:
				self.config["FPS"] = int(value)

	# Passing data to the main class
	def getConfig(self):
		return self.config