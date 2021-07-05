# Connection libraries
import pygame
import os

# Connecting files
from settings import *
from common import *

# Connecting classes
from launcher import Launcher
from play import Play

# Main class
class Main:
	def __init__(self):
		pygame.init()

		# Launcher screen
		self.screen = pygame.display.set_mode(SIZE)
		pygame.display.set_caption("Launcher")

		# Launcher icon
		launcherIcon = loadImage("launcher/icon.png")
		pygame.display.set_icon(launcherIcon)

		# Current folder
		self.currentFolder = os.getcwd()
		pathToProjects = os.getcwd() + "/projects/"

		# Boolean variables
		self.running = True

		# Clock
		self.clock = pygame.time.Clock()

		# Launcher
		self.launcher = Launcher()

		# Game screens for play.py
		self.screens = {}
		self.currentScreen = ""
		self.screens["main"] = False
		# self.screens[self.currentScreen]

		self.loop()

	# Handling events
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			for link in self.launcher.links:
				if event.type == pygame.MOUSEMOTION:
					if mouseCollision(link.xy, link.twh, event.pos):
						link.hover = True
					else: link.hover = False

	# Intermediant calculations
	def update(self):
		self.clock.tick(FPS)
		self.events()

	# Rendering game objects
	def render(self):
		self.screen.fill(QUARTZ)

		scImage(self.screen, "launcher/background.jpg", (0,0), SIZE)

		self.launcher.drawObjects(self.screen)

		pygame.display.update()

	# Gameloop
	def loop(self):
		while self.running:
			self.update()
			self.render()

	# Start project
	def startProject(self):
		project = Play(pathToProjects)

# Start launcher
Main()
pygame.quit()
