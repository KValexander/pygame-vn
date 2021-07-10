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
		# Path to current project
		self.config["pathToProject"] = self.folder
		
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

			# Screen directory
			elif line.find("screen_folder") != -1:
				self.config["screenFolder"] = value

			# Screen directory
			elif line.find("src_icon") != -1:
				self.config["srcIcon"] = value

			# System font
			elif line.find("system_font") != -1:
				self.config["systemFont"] = value

			# Own font
			elif line.find("own_font") != -1:
				self.config["ownFont"] = value

			# Type font
			elif line.find("type_font") != -1:
				self.config["typeFont"] = value

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

			# Play text coordinate
			elif line.find("play_text_coord") != -1:
				self.config["playTextCoord"] = defineSize(value, self.config["size"])

			# Play text width
			elif line.find("play_text_width") != -1:
				self.config["playTextWidth"] = defineOneSize(value, self.config["size"][0])

			# Play text size
			elif line.find("play_text_size") != -1:
				self.config["playTextSize"] = int(value)

			# Play text color
			elif line.find("play_text_color") != -1:
				self.config["playTextColor"] = defineColor(value)

			# Play line height
			elif line.find("play_line_height") != -1:
				self.config["playLineHeight"] = int(value)

		# Path to screen
		self.config["pathToScreen"] = self.config["pathToProject"] + self.config["screenFolder"]

		# Font
		if self.config["typeFont"] == "system": self.config["usedFont"] = self.config["systemFont"]
		elif self.config["typeFont"] == "own": self.config["usedFont"] = self.config["pathToProject"] + self.config["ownFont"]
		else: self.config["usedFond"] = None

	# Passing data to the main class
	def getConfig(self):
		return self.config