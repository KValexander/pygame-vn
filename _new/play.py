# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *

# Connections classes
from option import Option
from screen import Screen
from script import Script

# Play class
class Play:
	def __init__(self, folder):
		pygame.init()

		# Path to the project and clock
		self.folder = folder
		self.clock = pygame.time.Clock()

		# Boolean variables
		self.running = True

		# Script files data variables
		self.optionsdata = []
		self.screensdata = []
		self.scriptsdata = []

		# Variable dictionaries
		self.options = {}
		self.screens = {}
		self.scripts = {}

		# Retrieving script files data
		self.gettingFilesData()
		# Processing option data
		self.processingOption()
		# Launch window
		self.launchScreen()
		# Processing screen data
		self.processingScreen()
		# Start game
		self.gameloop()

	# Retrieving script files data
	def gettingFilesData(self):
		# Getting options
		file = codecs.open(self.folder + "options.vn", "r", "utf-8")
		self.optionsdata = clearLines(file.read().split("\n"))
		# Getting screens
		file = codecs.open(self.folder + "screens.vn", "r", "utf-8")
		self.screensdata = clearLines(file.read().split("\n"))
		# Getting script
		file = codecs.open(self.folder + "script.vn", "r", "utf-8")
		self.scriptsdata = clearLines(file.read().split("\n"))

	# Processing option data
	def processingOption(self):
		self.option  = Option(self.optionsdata)
		self.options = self.option.getConfig()

	# Processing screen data
	def processingScreen(self):
		self.screen = Screen(self.window, self.screensdata)
		self.screens = self.screen.getConfig()

	# Processing script data
	def processingScript(self):
		self.script = Script(self.window, self.scriptsdata)
		self.scripts = self.script.getConfig()

	# # Refresh screen
	# def refreshScreen(self):
	# 	for screen in self.screens:
	# 		self.screens[screen] = False
	# 	self.screens[self.currentScreen] = True

	# Launch window
	def launchScreen(self):
		# Game window
		self.window = pygame.display.set_mode(self.options["size"])
		pygame.display.set_caption(self.options["projectName"])

		# Game icon
		gameIcon = loadImage(self.folder + "gui/icon.png")
		pygame.display.set_icon(gameIcon)

	# Handling events
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

	# Intermediant calculation
	def update(self):
		self.clock.tick(self.options["FPS"])

		self.events()

	# Rendering game objects
	def render(self):
		self.window.fill(WHITE)

		pygame.display.update()

	# Gameloop
	def gameloop(self):
		while self.running:
			self.update()
			self.render()

