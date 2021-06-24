import pygame

from settings import *
from storage import *
from other import *

from interface import Interface

class Main:
	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode(SIZE)
		pygame.display.set_caption("VN")

		self.clock = pygame.time.Clock()
		self.running = False

		self.loading()

	def loading(self):
		self.start()

	def start(self):
		self.running = True
		self.loop()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: self.end()

	def update(self):
		self.clock.tick(FPS)

		self.events()

	def render(self):
		self.screen.fill((153, 204, 255))

		pygame.display.flip()

	def loop(self):
		while self.running:
			self.update()
			self.render()

	def end(self):
		self.running = False

Main()
pygame.quit()