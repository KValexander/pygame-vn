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
from saveload import SaveLoad

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
		# Event main screen
		self.mainscreenevent = False

		# Objects
		self.option = None
		self.screen = None
		self.script = None

		self.startScreen = ""
		self.playScreen = ""

		# Retrieving script files data
		self.gettingFilesData()
		# Processing option data
		self.processingOption()
		# Launch window
		self.launchScreen()
		# Processing screen data
		self.processingScreen()
		# Save/Load class
		self.saveload = SaveLoad(self.screen, self.option, self)
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
		self.playScreen = self.screen.config["playScreen"]
		self.refreshScreen(self.screen.config["startScreen"])

	# Processing script data
	def processingScript(self, state):
		self.refreshScreen(self.screen.config["playScreen"])
		if not "play" in self.currentScreen: return
		self.script = Script(self.window, self.scriptsdata, self.option.config, self.currentScreen["play"], self, state)

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
				# Check cells
				if "elements" in self.currentScreen:
					if "cells" in self.currentScreen["elements"]:
						if self.currentScreen["elements"]["cells"]!= None:
							print(self.currentScreen["elements"]["cells"])
							self.currentScreen["elements"]["cells"].checkCells()
				# Сall subscreen on screen startup
				if "startsubscreen" in self.currentScreen:
					self.refreshScreen(self.currentScreen["startsubscreen"])
				# Screen background loop sound
				if "loopsound" in self.currentScreen:
					src = self.option.config["pathToSounds"] + self.currentScreen["loopsound"]
					if os.path.exists(src):
						pygame.mixer.music.load(src)
						pygame.mixer.music.play(-1)
					else: pygame.mixer.music.stop()
				else: pygame.mixer.music.stop()
				# Screen background
				if "background" in self.currentScreen:
					src = self.option.config["pathToScreen"] + self.currentScreen["background"]
					if os.path.exists(src) == False or src.find(".") == -1:
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
					# Check cells
					if "cells" in self.currentSubscreen["elements"]:
						self.currentSubscreen["elements"]["cells"].checkCells()
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
					pygame.mixer.music.stop()
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
			self.processingScript("start")

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
			self.mainscreenevent = False

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
						if self.mainscreenevent == False:
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
				# Cells gover handling
				if "cells" in screen["elements"]:
					for cell in screen["elements"]["cells"].cells:
						if mouseCollision(cell["xy"], cell["wh"], e.pos):
							cell["hover"] = True
						else: cell["hover"] = False
					for point in screen["elements"]["cells"].points:
						if mouseCollision(point["xy"], point["wh"], e.pos):
							point["hover"] = True
						else: point["hover"] = False

		# Handling events
		if "actions" in screen:
			# Handling mouse events
			for jmouse in screen["actions"]["mouse"]:
				# Event handling
				if e.type == jmouse["type"]:
					if e.button == jmouse["button"]:
						self.mainscreenevent = True
						if jmouse["event"] == "call":
							self.refreshScreen(jmouse["return"])
						elif jmouse["event"] == "hide":
							self.hideScreen(jmouse["return"])
						elif jmouse["event"] == "close" or jmouse["event"] == "end" or jlink["event"] == "start":
								self.reservedCommands(jmouse["return"])

			# Handling cells events
			if "cells" in screen["actions"]:
				for cell in screen["elements"]["cells"].cells:
					if e.type == pygame.MOUSEBUTTONDOWN:
						if e.button == 1:
							if mouseCollision(cell["xy"], cell["wh"], e.pos):
								# Save data
								if screen["actions"]["cells"] == "save":
									if self.script != None:
										self.saveload.saveConfig(cell, self.script.config)
								# Load data
								elif screen["actions"]["cells"] == "load":
									self.saveload.loadConfig(cell)
				for point in screen["elements"]["cells"].points:
					if e.type == pygame.MOUSEBUTTONDOWN:
						if e.button == 1:
							if mouseCollision(point["xy"], point["wh"], e.pos):
								screen["elements"]["cells"].setPage(point["return"])

			# Handling link events
			for jlink in screen["actions"]["links"]:
				# Getting a link
				rlink = getElementByName(jlink["name"], screen["elements"]["links"])
				if rlink == None: break
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
				if ricon == None: break
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
					# Rendering cells
					if "cells" in self.currentScreen["elements"]:
						self.currentScreen["elements"]["cells"].draw(self.window)
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
						# Rendering cells
						if "cells" in self.currentSubscreen["elements"]:
							self.currentSubscreen["elements"]["cells"].draw(self.window)
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