# Connecting libraries
import pygame

# Connecting files
from settings import *
from storage import *
from other import *

# Connecting classes
from interface import Interface

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

		self.screen = pygame.display.set_mode(SIZE)
		pygame.display.set_caption("VN")

		self.clock = pygame.time.Clock()

		self.loading()

	# Loading data
	def loading(self):
		# Instances of classes
		self.loop = Loop()
		self.interface = Interface(self.screen)

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
			
			# Interface events
			self.interface.events(event, self.buttonAction)

	# Actions for buttons
	def buttonAction(self, name):
		# Exit button
		if name == "exit": self.end()
		# Start play button
		if name == "start":
			self.loop.mainloop = False
			self.loop.playloop = True

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

		# Rendering grid
		# drawGrid(self.screen)

		# Background image
		scImage(self.screen, "gui/background.jpg", (0,0), SIZE)

		if self.loop.mainloop:
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