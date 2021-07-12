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

			# Src icon
			elif line.find("src_icon") != -1:
				self.config["srcIcon"] = value

			# Character directory
			elif line.find("character_folder") != -1:
				self.config["characterFolder"] = value

			# Background directory
			elif line.find("background_folder") != -1:
				self.config["backgroundFolder"] = value

			# Image stock
			elif line.find("image_stock") != -1:
				self.config["imageStock"] = value

			# Character stock
			elif line.find("character_stock") != -1:
				self.config["characterStock"] = value

			# Background stock
			elif line.find("background_stock") != -1:
				self.config["backgroundStock"] = value

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
			elif line.find("t_text_size") != -1:
				self.config["textSize"] = int(value)

			# Text color
			elif line.find("t_text_color") != -1:
				self.config["textColor"] = defineColor(value)

			# Text line height
			elif line.find("t_text_line_height") != -1:
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

			# Cells outline color
			elif line.find("cells_outline_color") != -1:
				self.config["cellsOutlineColor"] = defineColor(value)

			# Cells background color
			elif line.find("cells_background_color") != -1:
				self.config["cellsBackgroundColor"] = defineColor(value)

			# Cells text color
			elif line.find("cells_text_color") != -1:
				self.config["cellsTextColor"] = defineColor(value)

			# Cells text size
			elif line.find("cells_text_size") != -1:
				self.config["cellsTextSize"] = int(value)

			# Cells margin
			elif line.find("cells_margin") != -1:
				self.config["cellsMargin"] = int(value)

			# Cells border
			elif line.find("cells_border") != -1:
				self.config["cellsBorder"] = int(value)

			# Condition text color
			elif line.find("condition_text_color") != -1:
				self.config["conditionTextColor"] = defineColor(value)

			# Condition background color
			elif line.find("condition_background_color") != -1:
				self.config["conditionBackgroundColor"] = defineColor(value)

			# Condition outline color
			elif line.find("condition_outline_color") != -1:
				self.config["conditionOutlineColor"] = defineColor(value)

			# Condition margin
			elif line.find("condition_margin") != -1:
				self.config["conditionMargin"] = int(value)

			# Condition border
			elif line.find("condition_border") != -1:
				self.config["conditionBorder"] = int(value)

			# Condition alpha
			elif line.find("condition_alpha") != -1:
				self.config["conditionAlpha"] = int(value)

			# Condition indentation
			elif line.find("condition_indentation") != -1:
				self.config["conditionIndentation"] = int(value)

		# Path to screen
		self.config["pathToScreen"] = self.config["pathToProject"] + self.config["screenFolder"]
		# Path to character
		self.config["pathToCharacter"] = self.config["pathToProject"] + self.config["characterFolder"]
		# Path to background
		self.config["pathToBackground"] = self.config["pathToProject"] + self.config["backgroundFolder"]
		# Path to image stock
		self.config["pathToImageStock"] = self.config["pathToScreen"] + self.config["imageStock"]
		# Path to character stock
		self.config["pathToCharacterStock"] = self.config["pathToScreen"] + self.config["characterStock"]
		# Path to background stock
		self.config["pathToBackgroundStock"] = self.config["pathToScreen"] + self.config["backgroundStock"]

		# Font
		if self.config["typeFont"] == "system": self.config["usedFont"] = self.config["systemFont"]
		elif self.config["typeFont"] == "own": self.config["usedFont"] = self.config["pathToProject"] + self.config["ownFont"]
		else: self.config["usedFond"] = None

	# Passing data to the main class
	def getConfig(self):
		return self.config