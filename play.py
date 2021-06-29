# Connecting libraries
import pygame
import codecs

# Connecting files
from settings import *
from storage import *
from other import *

# Play class
class Play:
	def __init__(self, screen, folder):
		self.screen = screen
		self.folder = folder

	# Loading data
	def loading(self):
		# Variables of text
		self.textmargin = 20
		self.textsize  	= 20
		self.textcolor	= BLACK
		self.textfont	= pygame.font.SysFont("arial", self.textsize)
		self.textloc	= (self.textmargin, HEIGHT - HEIGHT / 4 + self.textmargin)

		# Line counting variables
		self.currentStart = 0
		self.currentEnd = 0

		# Variable lines
		self.lines = []
		self.currentLine = ""
		self.line = self.textfont.render(str(self.currentLine), True, self.textcolor)

		# Boolean variables
		self.hide = False

		# Getting dialog box
		for surface in surfaces:
			if surface.name == "dialogbox":
				self.dialogBox = surface

		# Standard background image
		self.background = scLoadImage(self.folder + "assets/gui/backgroundplay.jpg", (WIDTH, HEIGHT))

		# Parsing the script file
		self.parseScript()

	# Parsing the script file
	def parseScript(self):
		# Getting script content
		script = codecs.open(self.folder + "script.txt")
		content = script.read()

		# Splitting a script
		define = content.split("vn start:")

		# Script lines
		self.lines = define[1].split("\n")
		self.currentEnd = len(self.lines)

		# Clearing script lines
		badChars = ['\r', '\n', '\t']
		for i in range(len(self.lines)):
			for char in badChars:
				self.lines[i] = self.lines[i].replace(char, "")

		# Clearing empty list items
		self.lines = [x for x in self.lines if x != '']

		self.scriptProcessing()

	# Processing script lines
	def scriptProcessing(self):
		# Current line
		self.currentLine = self.lines[self.currentStart]
		print(self.currentLine)

		# If this is a replica
		if self.currentLine == "\"" or self.currentLine == "\'":
			self.currentLine = removeChar(self.currentLine)
			self.line = self.textfont.render(str(self.currentLine), True, self.textcolor)

		print(self.line, self.textloc)

	# Handling events
	def events(self, e):
		# Handling mouse click
		if e.type == pygame.MOUSEBUTTONDOWN:
			pass

	# Rendering objects
	def draw(self):
		# Rendering background
		self.screen.blit(self.background, (0, 0))
		# Rendering text
		self.screen.blit(self.line, self.textloc)