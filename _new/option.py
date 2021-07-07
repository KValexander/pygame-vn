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

			# System font
			elif line.find("system_font") != -1:
				self.config["systemFont"] = value

			# Link color
			elif line.find("link_color") != -1:
				self.config["linkColor"] = defineColor(value)

			# Link aim
			elif line.find("link_aim") != -1:
				self.config["linkAim"] = defineColor(value)

			# Link selected
			elif line.find("link_selected") != -1:
				self.config["linkSelected"] = defineColor(value)

			# Link size
			elif line.find("link_size") != -1:
				self.config["linkSize"] = int(value)

			# Inscription color
			elif line.find("inscription_color") != -1:
				self.config["inscriptionColor"] = defineColor(value)

			# Inscription size
			elif line.find("inscription_size") != -1:
				self.config["inscriptionSize"] = int(value)

	# Passing data to the main class
	def getConfig(self):
		return self.config