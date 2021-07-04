# Connecting libraries
import pygame

# Connecting files
from settings import *
from storage import *
from other import *
from loop import *
from templates import *

# Create button
def createButton(name, value, tcolor, xy, wh, bcolor):
	button = Button(name, value, tcolor, xy, wh, bcolor)
	buttons.append(button)

# Create surface
def createSurface(name, color, alpha, xy, wh):
	surface = Surface(name, color, alpha, xy, wh)
	surfaces.append(surface)

# Create text
def createInscription(name, value, color, xy, size):
	inscription = Inscription(name, value, color, xy, size)
	inscriptions.append(inscription)

# Create link
def createLink():
	pass

# Create texture
def createTexture():
	pass

# Create objects
def create(case):
	buttons.clear()
	surfaces.clear()
	inscriptions.clear()

	if 	 case == "main": 	 createMain()
	elif case == "play": 	 createPlay()
	elif case == "settings": createSettings()
	elif case == "save": 	 createSave()
	elif case == "load": 	 createLoad()

# Create main screen objects
def createMain():
	createSurface("startscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
	createButton("play", "Начать игру", WHITE, gridSize((60, 180)), (180, 40), QUARTZ)
	createButton("load", "Загрузить", WHITE, gridSize((60, 230)), (180, 40), QUARTZ)
	createButton("settings", "Настройки", WHITE, gridSize((60, 280)), (180, 40), QUARTZ)
	createButton("exit", "Выйти", WHITE, gridSize((60, 330)), (180, 40), QUARTZ)

# Create play screen objects
def createPlay():
	createSurface("dialogbox", BLACK, 128, gridSize((0, HEIGHT - (HEIGHT / 4))), gridSize((WIDTH, 216)))

# Create settings screen objects
def createSettings():
	createSurface("startscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
	createSurface("settingscreen", BLACK, 90, gridSize((320, 0)), gridSize((WIDTH - 320, HEIGHT)))

	createButton("play", "Начать игру", WHITE, gridSize((60, 180)), (180, 40), QUARTZ)
	createButton("load", "Загрузить", WHITE, gridSize((60, 230)), (180, 40), QUARTZ)
	createButton("settings", "Настройки", WHITE, gridSize((60, 280)), (180, 40), QUARTZ)
	createButton("exit", "Выйти", WHITE, gridSize((60, 330)), (180, 40), QUARTZ)
	
	createInscription("settingscreen", "Настройки", WHITE, gridSize((380, 32)), 50)

# Create load screen objects
def createLoad():
	createSurface("startscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
	createSurface("loadscreen", BLACK, 90, gridSize((320, 0)), gridSize((WIDTH - 320, HEIGHT)))

	createButton("play", "Начать игру", WHITE, gridSize((60, 180)), (180, 40), QUARTZ)
	createButton("load", "Загрузить", WHITE, gridSize((60, 230)), (180, 40), QUARTZ)
	createButton("settings", "Настройки", WHITE, gridSize((60, 280)), (180, 40), QUARTZ)
	createButton("exit", "Выйти", WHITE, gridSize((60, 330)), (180, 40), QUARTZ)

	createInscription("loadscreen", "Загрузить", WHITE, gridSize((380, 32)), 50)

# Create play menu objects
def createMenu():
	pass

# Render current interface elements 
def drawInterface(screen):
	# Rendering surfaces
	for surface in surfaces:
		if surface.name == "dialogbox": continue
		surface.draw(screen)

	# Rendering buttons
	for button in buttons:
		button.draw(screen)

	# Rendering inscriptions
	for inscription in inscriptions:
		inscription.draw(screen)