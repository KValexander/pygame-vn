# Connection libraries
import pygame
import codecs
import os

# Connecting files
from settings import *
from common import *

# Connecting classes
from launcher import Launcher
from create import Create
from play import Play

# Main class
class Main:
	def __init__(self):
		pygame.init()

		# Setting variables
		self.pathToProjects = ""

		# Getting launcher settings
		self.getLauncherSettings()

		# Launcher window
		self.window = pygame.display.set_mode(SIZE)
		pygame.display.set_caption("Launcher")

		# Launcher icon
		launcherIcon = loadImage("launcher/icon.png")
		pygame.display.set_icon(launcherIcon)

		# Current folder
		self.currentFolder = os.getcwd()

		# Boolean variables
		self.running = True

		# Clock
		self.clock = pygame.time.Clock()

		# Launcher
		self.launcher = Launcher()

		# Create
		self.create = Create(self.pathToProjects)

		# Path
		self.path = ""

		# Gameloop
		self.loop()

	# Getting launcher settings
	def getLauncherSettings(self):
		settings = codecs.open("launcher/settings.vn", "r", "utf-8")
		content = clearLines(settings.read().split("\n"))
		for line in content:
			line = line.replace(" ", "")
			setting, value = line.split("=")
			if setting == "PATHTOPROJECTS": self.pathToProjects = value

		self.pathToProjects = os.getcwd() + "/projects/"

	# Handling events
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.end()

			# Handling buttons
			for button in self.launcher.buttons:
				if event.type == pygame.MOUSEMOTION:
					if mouseCollision(button.xy, button.wh, event.pos):
						button.hover = True
					else: button.hover = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					if mouseCollision(button.xy, button.wh, event.pos):
						button.click = True
						self.buttonActions(button)
					else: button.click = False

			# Handling links
			for link in self.launcher.links:
				if event.type == pygame.MOUSEMOTION:
					if mouseCollision(link.xy, link.twh, event.pos):
						link.hover = True
					else: link.hover = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					if mouseCollision(link.xy, link.twh, event.pos):
						link.selected = True
					else: link.selected = False

	# Button actions
	def buttonActions(self, button):
		# Start selected project
		if button.name == "startproject":
			# Getting the name of the selected project
			projectname = ""
			for link in self.launcher.links:
				if link.selected == True: projectname = link.rtrn
			if projectname == "": return
			self.startProject(projectname)
			
		# Create new project
		elif button.name == "createproject":
			self.create.createProject("new")
			self.launcher.createProjectList()

		# Updating the list of projects
		elif button.name == "updatelistcprojects":
			self.launcher.createProjectList()

		# Deleting the selected project
		elif button.name == "deleteproject":
			projectname = ""
			for link in self.launcher.links:
				if link.selected == True: projectname = link.rtrn
			if projectname == "": return
			self.create.deleteProject(projectname)
			self.launcher.createProjectList()

	# Intermediant calculations
	def update(self):
		self.clock.tick(FPS)
		self.events()

	# Rendering game objects
	def render(self):
		self.window.fill(WHITE)

		# scImage(self.window, "launcher/background.jpg", (0,0), SIZE)

		self.launcher.drawObjects(self.window)

		pygame.display.update()

	# Gameloop
	def loop(self):
		while self.running:
			self.update()
			self.render()

	# Start project
	def startProject(self, projectName):
		self.path = self.pathToProjects + projectName
		self.end()

	# Turn off the launcher
	def end(self):
		self.running = False

# Start launcher
main = Main()
path = main.path
pygame.quit()

if path != "":
	# Start project
	Play(path)
	pygame.quit()