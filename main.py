# Connecting libraries
import pygame

# Connecting files
from settings import *
from storage import *
from other import *

# Connecting classes
from interface import Interface
from play import Play

# Loop class
class Loop:
	def __init__(self):
		self.running 		= False
		self.mainloop 		= False
		self.playloop 		= False
		self.loadloop 		= False
		self.saveloop 		= False
		self.settingsloop 	= False

# Main class
class Main:
	def __init__(self):
		pygame.init()

		# Game screen
		self.screen = pygame.display.set_mode(SIZE)
		pygame.display.set_caption("VN")

		# Project folder
		self.folder = "C:/gamemake/VN/vn/"

		# Clock
		self.clock = pygame.time.Clock()

		self.loading()

	# Loading data
	def loading(self):
		# Instances of classes
		self.loop 		= Loop()
		self.interface 	= Interface(self.screen, self.folder)
		self.play 		= Play(self.screen, self.folder, self.loop)

		# Start game
		self.start()

	# Game start
	def start(self):
		self.loop.running	= True
		self.loop.mainloop 	= True
		self.gameloop()

	# Handling events
	def events(self):
		for event in pygame.event.get():
			# Disabling the game
			if event.type == pygame.QUIT:
				self.end()

			# Playing events
			if self.loop.playloop:
				self.play.events(event)
			
			# Interface events
			self.interface.events(event, self.buttonAction)

	# Actions for buttons
	def buttonAction(self, name):
		screen = ""

		# Exit button
		if name == "exit":
			self.end()
		# Start play button
		if name == "play":
			self.loop.mainloop = False
			self.loop.playloop = True
			self.interface.createPlay()
			self.play.loading()
			screen = "play"
		# Load button
		if name == "load":
			self.loop.mainloop = False
			self.loop.loadloop = True
			screen = "load"
		# Settings button
		if name == "settings":
			self.loop.mainloop = False
			self.loop.settingsloop = True
			screen = "settings"

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
		if self.loop.mainloop:
			# Background image
			scImage(self.screen, self.folder + "assets/gui/backgroundmenu.jpg", (0,0), SIZE)

		# Rendering play screen
		if self.loop.playloop:
			self.play.draw()
			
		# Rendering grid
		# drawGrid(self.screen)

		# Rendering interface
		self.interface.draw()

		pygame.display.update()

	# Gameloop
	def gameloop(self):
		while self.loop.running:
			self.update()
			self.render()

	# End of the game
	def end(self):
		self.loop.running = False

Main()
pygame.quit()