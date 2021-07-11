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

		# Check subscreens call type
		self.subcallcheck = False
		# Event main lock
		self.eventmainlock = False

		# Objects
		self.option = None
		self.screen = None
		self.script = None

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
		self.option = Option(self.optionsdata, self.folder)

	# Processing screen data
	def processingScreen(self):
		self.screen = Screen(self.window, self.screensdata, self.option.config)
		self.startScreen = self.screen.config["startScreen"]
		self.refreshScreen(self.startScreen)

	# Processing script data
	def processingScript(self):
		self.refreshScreen(self.screen.config["playScreen"])
		if not "play" in self.currentScreen: return
		self.script = Script(self.window, self.scriptsdata, self.option.config, self.currentScreen["play"], self)

	# Refresh screen
	def refreshScreen(self, screen):
		# Reserved Commands
		if screen == "end" or screen == "close" or screen == "start": self.reservedCommands(screen)
		# Handling refresh screen
		else:
			# Check screen
			if screen in self.screen.config:
				# Check configurations screen
				if not "background" in self.screen.config[screen]: return
				self.currentScreen = self.screen.config[screen]
				self.currentScreen["display"] = True
				self.currentScreen["subdisplay"] = False
				self.subbackground = None
				self.eventmainlock = False
				# Сall subscreen on screen startup
				if "startsubscreen" in self.currentScreen:
					self.refreshScreen(self.currentScreen["startsubscreen"])
				# Screen background
				if "background" in self.currentScreen:
					src = self.folder + self.option.config["screenFolder"] + self.currentScreen["background"]
					if os.path.exists(src) == False:
						src = self.option.config["pathToBackgroundStock"]
					self.background = scLoadImage(src, self.option.config["size"])
			# Sub screen
			else:
				# Getting, check main screen and check subscreen by calltype
				subscreen, screen = screen, getMainScreen(screen, self.screen.config)
				if screen == None: return
				if not "calltype" in self.screen.config[screen]["subscreens"][subscreen]: return

				# Subscreen call type
				calltype = self.screen.config[screen]["subscreens"][subscreen]["calltype"]

				# Subscreen call type check
				# Local call
				if calltype == "local":
					# Checking for a subscreen
					if self.currentScreen == self.screen.config[screen]:
						self.subcallcheck = True
				# Global type
				elif calltype == "global":
					self.subcallcheck = True
				# Global with the challenge of the main
				elif calltype == "cls":
					self.refreshScreen(screen)
					self.subcallcheck = True

				# Checking for a subscreen
				if self.subcallcheck:
					self.subcallcheck = False
					self.currentScreen["subdisplay"] = True
					self.currentSubscreen = self.screen.config[screen]["subscreens"][subscreen]
					# Event main lock
					if "eventmainlock" in self.currentSubscreen: self.eventmainlock = True
					else: self.eventmainlock = False
					# Subscreen background
					if "background" in self.currentSubscreen:
						src = self.folder + self.option.config["screenFolder"] + self.currentSubscreen["background"]
						if os.path.exists(src) == False:
							src = self.option.config["pathToBackgroundStock"]
						self.subbackground = scLoadImage(src, self.option.config["size"])

	# Hiding the screen
	def hideScreen(self, screen):
		# Reserved Commands
		if screen == "end" or screen == "close" or screen == "start": self.reservedCommands(screen)
		# Handling hide screen
		else:
			# Check main screen
			if screen in self.screen.config:
				if self.currentScreen == self.screen.config[screen]:
					# Clear screen
					self.currentScreen["display"] = False
					self.currentScreen["subdisplay"] = False
			else:
				# Getting and check main screen
				subscreen, screen = screen, getMainScreen(screen, self.screen.config)
				if screen == None: return

				# Check sub screen
				if self.currentSubscreen == self.screen.config[screen]["subscreens"][subscreen]:
					# Clear screen
					self.currentScreen["subdisplay"] = False
					self.subbackground = None
					self.eventmainlock = False

	# Reserved Commands
	def reservedCommands(self, command):
		if command == "end": self.running = False
		elif command == "close":
			self.currentScreen["subdisplay"] = False
			self.subbackground = None
			self.eventmainlock = False
		elif command == "start":
			self.processingScript()

	# Launch window
	def launchScreen(self):
		# Game window
		self.window = pygame.display.set_mode(self.option.config["size"])
		pygame.display.set_caption(self.option.config["projectName"])

		# Game icon
		gameIcon = loadImage(self.folder + self.option.config["srcIcon"])
		pygame.display.set_icon(gameIcon)

	# Handling events
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			# Screen events
			if self.currentScreen["display"]:
				if self.subbackground == None and self.eventmainlock == False:
					# Handling actions for interface elements
					self.actions(event, self.currentScreen)
					# Handling play events
					if "play" in self.currentScreen and self.script != None:
						self.script.events(event)

				# Subscreen events
				if self.currentScreen["subdisplay"]:
					if self.currentSubscreen["display"]:
						# Handling actions for interface elements
						self.actions(event, self.currentSubscreen)

	# Handling actions for interface elements
	def actions(self, e, screen):
		# Standard events
		if "elements" in screen:
			if e.type == pygame.MOUSEMOTION:
				# Link hover handling
				for link in screen["elements"]["links"]:
					if mouseCollision(link.xy, link.twh, e.pos):
						link.hover = True
					else: link.hover = False

		# Handling events
		if "actions" in screen:
			# Handling mouse events
			for jmouse in screen["actions"]["mouse"]:
				# Event handling
				if e.type == jmouse["type"]:
					if e.button == jmouse["button"]:
						if jmouse["event"] == "call":
							self.refreshScreen(jmouse["return"])
						elif jmouse["event"] == "hide":
							self.hideScreen(jmouse["return"])
						elif jmouse["event"] == "close" or jmouse["event"] == "end" or jlink["event"] == "start":
								self.reservedCommands(jmouse["return"])

			# Handling link events
			for jlink in screen["actions"]["links"]:
				# Getting a link
				rlink = getElementByName(jlink["name"], screen["elements"]["links"])
				if rlink == None: return
				# Event handling
				if e.type == jlink["type"]:
					if e.button == jlink["button"]:
						if mouseCollision(rlink.xy, rlink.twh, e.pos):
							if jlink["event"] == "call":
								self.refreshScreen(jlink["return"])
							elif jlink["event"] == "hide":
								self.hideScreen(jlink["return"])
							elif jlink["event"] == "close" or jlink["event"] == "end" or jlink["event"] == "start":
								self.reservedCommands(jlink["return"])

			# Handling icons events
			for jicon in screen["actions"]["icons"]:
				# Getting icon
				ricon = getElementByName(jicon["name"], screen["elements"]["icons"])
				if ricon == None: return
				# Event handling
				if e.type == jicon["type"]:
					if mouseCollision(ricon.xy, ricon.wh, e.pos):
						# Mousemotion
						if jicon["button"] == None:
							if jicon["event"] == "hover":
								ricon.setHoverImage(jicon["src"])
								ricon.hover = True
						# Mousebuttondown
						elif e.button == jicon["button"]:
							if jicon["event"] == "call":
								self.refreshScreen(jicon["return"])
							elif jicon["event"] == "hide":
								self.hideScreen(jicon["return"])
							elif jicon["event"] == "close" or jicon["event"] == "end" or jlink["event"] == "start":
									self.reservedCommands(jicon["return"])
					else: ricon.hover = False

	# Intermediant calculation
	def update(self):
		self.clock.tick(self.option.config["FPS"])
		self.events()

	# Rendering game objects
	def render(self):
		self.window.fill(WHITE)

		# Rendering screen
		if self.currentScreen["display"]:
			if self.subbackground == None:
				# Rendering background
				if "play" in self.currentScreen and self.script != None:
					self.script.background(self.window)
				elif "background" in self.currentScreen:
					drawImage(self.window, self.background, (0, 0))

				# Rendering elements
				if "elements" in self.currentScreen:
					# Rendering surfaces
					for surface in self.currentScreen["elements"]["surfaces"]:
						surface.draw(self.window)
					# Rendering surfaces
					for texture in self.currentScreen["elements"]["textures"]:
						texture.draw(self.window)
					# Rendering inscriptions
					for inscription in self.currentScreen["elements"]["inscriptions"]:
						inscription.draw(self.window)
					# Rendering texts
					for text in self.currentScreen["elements"]["texts"]:
						text.draw(self.window)
					# Rendering links
					for link in self.currentScreen["elements"]["links"]:
						link.draw(self.window)
					# Rendering icons
					for icon in self.currentScreen["elements"]["icons"]:
						icon.draw(self.window)
				
				# Rendering script
				if "play" in self.currentScreen and self.script != None:
						self.script.draw(self.window)

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
						# Rendering surfaces
						for texture in self.currentSubscreen["elements"]["textures"]:
							texture.draw(self.window)
						# Rendering inscriptions
						for inscription in self.currentSubscreen["elements"]["inscriptions"]:
							inscription.draw(self.window)
						# Rendering texts
						for text in self.currentSubscreen["elements"]["texts"]:
							text.draw(self.window)
						# Rendering links
						for link in self.currentSubscreen["elements"]["links"]:
							link.draw(self.window)
						# Rendering icons
						for icon in self.currentSubscreen["elements"]["icons"]:
							icon.draw(self.window)

		pygame.display.update()

	# Gameloop
	def gameloop(self):
		while self.running:
			self.update()
			self.render()