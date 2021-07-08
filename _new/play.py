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

		# Current screen, subscreen, background and subbackground
		self.currentScreen = {}
		self.currentSubscreen = {}
		self.background = None
		self.subbackground = None

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
		self.screen = Screen(self.window, self.screensdata, self.option.config)
		self.refreshScreen(self.screen.startScreen)

	# Processing script data
	def processingScript(self):
		self.script = Script(self.window, self.scriptsdata, self.option.config)

	# Refresh screen
	def refreshScreen(self, screen):
		if screen == "end": self.running = False
		else:
			# Screen
			if screen in self.screen.config:
				self.currentScreen = self.screen.config[screen]
				# Screen background
				if "background" in self.currentScreen:
					src = self.folder + "gui/" + self.currentScreen["background"]
					self.background = scLoadImage(src, self.option.config["size"])
			# Sub screen
			else:
				# Getting and check main screen
				subscreen, screen = screen, getMainScreen(screen, self.screen.config)
				if screen == None: return

				# Checking for a subscreen
				if self.currentScreen == self.screen.config[screen]:
					self.currentScreen["subdisplay"] = True
					self.currentSubscreen = self.screen.config[screen]["subscreens"][subscreen]
					# Subscreen background
					if "background" in self.currentSubscreen:
						src = self.folder + "gui/" + self.currentSubscreen["background"]
						self.subbackground = scLoadImage(src, self.option.config["size"])

	# Hiding the screen
	def hideScreen(self, screen):
		# Check main screen
		if screen in self.screen.config:
			if self.currentScreen == self.screen.config[screen]:
				# Clear screen
				self.currentScreen["subdisplay"] = False
				self.currentSubscreen.clear()
				self.currentScreen.clear()
		else:
			# Getting and check main screen
			subscreen, screen = screen, getMainScreen(screen, self.screen.config)
			if screen == None: return

			# Check sub screen
			if self.currentSubscreen == self.screen.config[screen]["subscreens"][subscreen]:
				# Clear screen
				self.currentScreen["subdisplay"] = False

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

			# Screen events
			if self.currentScreen["display"]:
				# Standard events
				if "elements" in self.currentScreen:
					if event.type == pygame.MOUSEMOTION:
						# Link hover handling 
						for link in self.currentScreen["elements"]["links"]:
							if mouseCollision(link.xy, link.twh, event.pos):
								link.hover = True
							else: link.hover = False

				# Hanging events
				if "actions" in self.currentScreen:
					# Handling Link Events
					for jlink in self.currentScreen["actions"]["links"]:
						# Getting a link
						rlink = getElementByName(jlink["name"], self.currentScreen["elements"]["links"])
						if rlink == None: return
						# Event handling
						if event.type == jlink["type"]:
							if event.button == jlink["button"]:
								if mouseCollision(rlink.xy, rlink.twh, event.pos):
									if jlink["event"] == "call":
										self.refreshScreen(jlink["return"])

			# Subscreen events
			if self.currentScreen["subdisplay"]:
				if self.currentSubscreen["display"]:
					# Standard events
					if "elements" in self.currentSubscreen:
						if event.type == pygame.MOUSEMOTION:
							# Link hover handling 
							for link in self.currentSubscreen["elements"]["links"]:
								if mouseCollision(link.xy, link.twh, event.pos):
									link.hover = True
								else: link.hover = False

					# Hanging events
					if "actions" in self.currentSubscreen:
						# Handling Link Events
						for jlink in self.currentSubscreen["actions"]["links"]:
							# Getting a link
							rlink = getElementByName(jlink["name"], self.currentSubscreen["elements"]["links"])
							if rlink == None: return
							# Event handling
							if event.type == jlink["type"]:
								if event.button == jlink["button"]:
									if mouseCollision(rlink.xy, rlink.twh, event.pos):
										if jlink["event"] == "call":
											self.refreshScreen(jlink["return"])
										if jlink["event"] == "hide":
											self.hideScreen(jlink["return"])

	# Intermediant calculation
	def update(self):
		self.clock.tick(self.option.config["FPS"])

		self.events()

	# Rendering game objects
	def render(self):
		self.window.fill(WHITE)

		# Rendering screen
		if self.currentScreen["display"]:
			# Rendering background
			if "background" in self.currentScreen:
				drawImage(self.window, self.background, (0, 0))

			# Rendering elements
			if "elements" in self.currentScreen:
				# Rendering surfaces
				for surface in self.currentScreen["elements"]["surfaces"]:
					surface.draw(self.window)
				# Rendering inscriptions
				for inscription in self.currentScreen["elements"]["inscriptions"]:
					inscription.draw(self.window)
				# Rendering links
				for link in self.currentScreen["elements"]["links"]:
					link.draw(self.window)

			# Rendering subscreen
			if self.currentScreen["subdisplay"]:
				if self.currentSubscreen["display"]:

					# Rendering background
					if "background" in self.currentSubscreen:
						drawImage(self.window, self.subbackground, (0,0))

					# Rendering elements
					if "elements" in self.currentSubscreen:
						# Rendering surfaces
						for surface in self.currentSubscreen["elements"]["surfaces"]:
							surface.draw(self.window)
						# Rendering inscriptions
						for inscription in self.currentSubscreen["elements"]["inscriptions"]:
							inscription.draw(self.window)
						# Rendering links
						for link in self.currentSubscreen["elements"]["links"]:
							link.draw(self.window)

		pygame.display.update()

	# Gameloop
	def gameloop(self):
		while self.running:
			self.update()
			self.render()

