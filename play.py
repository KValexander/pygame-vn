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

		# Current screen and background
		self.currentScreen = {}
		self.background = ""

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
		self.option = Option(self.optionsdata)

	# Processing screen data
	def processingScreen(self):
		self.screen = Screen(self.window, self.screensdata)
		self.refreshScreen(self.screen.startScreen)

	# Processing script data
	def processingScript(self):
		self.script = Script(self.window, self.scriptsdata)

	# Refresh screen
	def refreshScreen(self, screen):
		self.currentScreen = self.screen.config[screen]
		if "background" in self.currentScreen:
			src = self.folder + "gui/" + self.currentScreen["background"]
			self.background = scLoadImage(src, self.option.config["size"])

	# Launch window
	def launchScreen(self):
		# Game window
		self.window = pygame.display.set_mode(self.option.config["size"])
		pygame.display.set_caption(self.option.config["projectName"])

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
		self.clock.tick(self.option.config["FPS"])

		self.events()

	# Rendering game objects
	def render(self):
		self.window.fill(WHITE)

		# Rendering background
		if self.currentScreen["display"]:
			if "background" in self.currentScreen:
				drawImage(self.window, self.background, (0, 0))

		pygame.display.update()

	# Gameloop
	def gameloop(self):
		while self.running:
			self.update()
			self.render()

