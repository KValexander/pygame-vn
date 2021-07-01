# Connect files
from configs import *

# Arrays
items = []
selectedItems = []

# Interface arrays
buttons = []
surfaces = []

# Getting item
def getItemById(ident):
	for item in items:
		if item.id == ident:
			return item

# Removing item
def removeItem(item):
	items.remove(item)

# Removing items
def removeItems():
	for item in selectedItems:
		items.remove(item)
	clearSelection()

# Adding items in selection items
def addSelection(item):
	item.selected = True
	selectedItems.append(item)

# Clear selected items
def clearSelection():
	for item in items:
		item.selected = False
	selectedItems.clear()

# Clear buttons
def clearButtons():
	buttons.clear()

# Clear surfaces
def clearSurfaces():
	surfaces.clear()


# Import templates
from templates import Worker

# Adding item
def addItem(case, counter, x, y, faction):
	if(case == "worker"):
		item = Worker(counter, x, y, faction)
	if(case == "soldier"):
		item = Soldier(counter, x, y, faction)

	items.append(item)
