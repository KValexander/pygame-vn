# Connecting libraries
import pygame
import os

# Connecting files
from settings import *
from storage import *
from other import *
from loop import *
from interface import *

# Connecting classes
from play import Play

# Main class
class Main:
	def __init__(self):
		pygame.init()

		# Game screen
		self.screen = pygame.display.set_mode(SIZE)
		pygame.display.set_caption("VN")

		# Getting the current directory
		currentFolder = os.getcwd()
		# Project folder
		self.folder = currentFolder + "/vn/"

		# Game icon
		gameIcon = loadImage(self.folder + "assets/icon.png")
		pygame.display.set_icon(gameIcon)

		# Clock
		self.clock = pygame.time.Clock()

		self.loading()

	# Loading data
	def loading(self):
		# Instances of classes
		self.play = Play(self.screen, self.folder)

		# Start game
		self.start()

	# Game start
	def start(self):
		loop.running	= True
		loop.mainloop 	= True
		self.gameloop()

	# Handling events
	def events(self):
		for event in pygame.event.get():
			# Disabling the game
			if event.type == pygame.QUIT:
				self.end()

			# Playing events
			if loop.playloop:
				self.play.events(event)

			# Handling button events
			for button in buttons:
				# Handling button click
				if event.type == pygame.MOUSEBUTTONDOWN:
					if button.rect.collidepoint(event.pos):
						create(self.buttonAction(button.name))

				# Hovering over the button
				if event.type == pygame.MOUSEMOTION:
					if(button.rect.collidepoint(event.pos)):
						button.hover = True
					else: button.hover = False

			# Handling cells events
			for cell in cells:
				cell.events(event)

	# Actions for buttons
	def buttonAction(self, name):
		screen = ""

		# Exit button
		if name == "exit": self.end()
		# Start play button
		if name == "play":
			createPlay()
			self.play.loading()
			screen = "play"
		# Load button
		if name == "load":
			if loop.loadloop:
				screen = "main"
			else:
				screen = "load"
		# Settings button
		if name == "settings":
			if loop.settingsloop:
				screen = "main"
			else:
				screen = "settings"
		# Back to main menu
		if name == "back":
			screen = "main"

		return screen

	# Intermediant calculations
	def update(self):
		# Updates per second
		self.clock.tick(FPS)

		# Handling events
		self.events()

	# Rendering game objects
	def render(self):
		# Background color
		self.screen.fill(WHITE)
		
		# Rendering main screen
		if loop.mainloop or loop.loadloop or loop.settingsloop:
			# Background image
			scImage(self.screen, self.folder + "assets/gui/backgroundmenu.jpg", (0,0), SIZE)

		# Rendering play screen
		if loop.playloop:
			self.play.draw()

		# Rendering interface
		drawInterface(self.screen)

		pygame.display.update()

	# Gameloop
	def gameloop(self):
		while loop.running:
			self.update()
			self.render()

	# End of the game
	def end(self):
		loop.running = False

Main()
pygame.quit()