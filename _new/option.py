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
	def __init__(self, data, folder):
		self.data 	= data
		self.folder = folder
		self.config = {}

		# Data processing
		self.dataProcessing()

	# Data processing
	def dataProcessing(self):
		for line in self.data:
			if commonCommands(line) == False: continue
			line = line.replace(" ", "")
			name, value = line.split("=")

			# Path to current project
			self.config["pathToProject"] = self.folder

			# Screen resolution
			if line.find("window_size") != -1:
				self.config["size"] = defineResolution(value)

			# The name of the project
			elif line.find("project_name") != -1:
				self.config["projectName"] = removeChar(value)

			# FPS
			elif line.find("fps") != -1:
				self.config["FPS"] = int(value)

			# Screen directory
			elif line.find("screen_folder") != -1:
				self.config["screenFolder"] = value

			# Screen directory
			elif line.find("src_icon") != -1:
				self.config["srcIcon"] = value

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

			# Text size
			elif line.find("text_size") != -1:
				self.config["textSize"] = int(value)

			# Text color
			elif line.find("text_color") != -1:
				self.config["textColor"] = defineColor(value)

			# Text line height
			elif line.find("text_line_height") != -1:
				self.config["textLineHeight"] = int(value)

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