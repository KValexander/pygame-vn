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

# Create cell 
def createCell(name, xy, wh):
	cell = Cell(name, xy, wh)
	cells.append(cell)

# Create objects
def create(case):
	if case == None: return
	cells.clear()
	links.clear()
	buttons.clear()
	textures.clear()
	surfaces.clear()
	inscriptions.clear()
	loop.loadloop 		= False
	loop.playloop 		= False
	loop.menuloop 		= False
	loop.saveloop 		= False
	loop.settingsloop 	= False
	loop.mainloop  		= False

	if 	 case == "main":
		loop.mainloop = True
		createMain()
	elif case == "play":
		loop.playloop = True
		createPlay()
	elif case == "save":
		loop.saveloop = True
		createSave()
	elif case == "load":
		loop.loadloop = True
		createLoad()
	elif case == "settings":
		loop.settingsloop = True
		createSettings()

# Create main screen objects
def createMain():
	createSurface("startscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
	createButton("play", "Начать игру", WHITE, gridSize((60, 180)), (180, 40), QUARTZ)
	createButton("load", "Загрузить", WHITE, gridSize((60, 230)), (180, 40), QUARTZ)
	createButton("settings", "Настройки", WHITE, gridSize((60, 280)), (180, 40), QUARTZ)
	createButton("exit", "Выйти", WHITE, gridSize((60, 330)), (180, 40), QUARTZ)

# Create play screen objects
def createPlay():
	createSurface("hmenuscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
	createSurface("hsavescreen", BLACK, 90, gridSize((320, 0)), gridSize((WIDTH - 320, HEIGHT)))
	createButton("hmenu", "Главное меню", WHITE, gridSize((60, 180)), (180, 40), QUARTZ)
	createButton("hsave", "Сохранить", WHITE, gridSize((60, 230)), (180, 40), QUARTZ)
	createButton("hload", "Загрузить", WHITE, gridSize((60, 280)), (180, 40), QUARTZ)
	createButton("hexit", "Выйти", WHITE, gridSize((60, 330)), (180, 40), QUARTZ)

	createSurface("dialogbox", BLACK, 128, gridSize((0, HEIGHT - (HEIGHT / 4))), gridSize((WIDTH, 216)))

# Create settings screen objects
def createSettings():
	createSurface("startscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
	createSurface("settingscreen", BLACK, 90, gridSize((320, 0)), gridSize((WIDTH - 320, HEIGHT)))

	createButton("play", "Начать игру", WHITE, gridSize((60, 180)), (180, 40), QUARTZ)
	createButton("load", "Загрузить", WHITE, gridSize((60, 230)), (180, 40), QUARTZ)
	createButton("settings", "Настройки", WHITE, gridSize((60, 280)), (180, 40), QUARTZ)
	createButton("exit", "Выйти", WHITE, gridSize((60, 330)), (180, 40), QUARTZ)
	
	createInscription("settingscreen", "Настройки", WHITE, gridSize((356, 32)), 50)

# Create load screen objects
def createLoad():
	createSurface("startscreen", BLACK, 90, (0,0), gridSize((300, HEIGHT)))
	createSurface("loadscreen", BLACK, 90, gridSize((320, 0)), gridSize((WIDTH - 320, HEIGHT)))

	createButton("play", "Начать игру", WHITE, gridSize((60, 180)), (180, 40), QUARTZ)
	createButton("load", "Загрузить", WHITE, gridSize((60, 230)), (180, 40), QUARTZ)
	createButton("settings", "Настройки", WHITE, gridSize((60, 280)), (180, 40), QUARTZ)
	createButton("exit", "Выйти", WHITE, gridSize((60, 330)), (180, 40), QUARTZ)

	createInscription("loadscreen", "Загрузить", WHITE, gridSize((356, 32)), 50)

	xy = [350, 120]
	for i in range(9):
		if i == 0:
			pass
		elif i % 3 == 0:
			xy[0] = 350
			xy[1] += 200
		else:
			xy[0] += 220
		createCell("s_"+str(i), (xy[0], xy[1]), (200, 150))

# Create play menu objects
def createMenu():
	pass

# Render current interface elements 
def drawInterface(screen):
	# Rendering surfaces
	for surface in surfaces:
		if surface.name == "dialogbox" or surface.name == "hmenuscreen" or surface.name == "hsavescreen": continue
		surface.draw(screen)

	# Rendering buttons
	for button in buttons:
		if button.name == "hmenu" or button.name == "hsave" or button.name == "hexit" or button.name == "hload": continue
		button.draw(screen)

	# Rendering cells
	for cell in cells:
		cell.draw(screen)

	# Rendering links
	for link in links:
		link.draw(screen)

	# Rendering inscriptions
	for inscription in inscriptions:
		if inscription.name == "hsavescreen": continue
		inscription.draw(screen)