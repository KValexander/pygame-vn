# Connect files
from configs import *

# Handling edges collision
def edgesCollision(item):
	if item.rect.x <= 0: item.rect.x += item.speed
	if item.rect.x + item.rect.width >= WIDTH: item.rect.y -= item.speed
	if item.rect.y <= 0: item.rect.y += item.speed
	if item.rect.y + item.rect.height >= HEIGHT: item.rect.y -= item.speed

# Handling circle collision
def circleCollision(circle, crle):
	if( circle.rect.center[0] + circle.radius >= crle.rect.center[0]
		and crle.rect.center[0] + crle.radius >= circle.rect.center[0]
		and circle.rect.center[1] + circle.radius >= crle.rect.center[1]
		and crle.rect.center[1] + crle.radius >= circle.rect.center[1]):
		return True
	else: return False

# Handling mouse collision
def mouseCollision(item, mousePos):
	x, y = mousePos
	if( item.x < x and (item.x + item.width) > x
		and item.x < y and (item.y + item.height ) > y):
		return True
	else: return False

# Handling select collision
def selectCollision(selRect, item):
	# The wonders of mathematics
	if( #TopLeft
		selRect.x < item.rect.x and (selRect.x + selRect.width) > (item.rect.x + item.rect.width)
		and selRect.y < item.rect.y and (selRect.y + selRect.height) > (item.rect.y + item.rect.height) or
		# BottomLeft
		selRect.x < item.rect.x and (selRect.x + selRect.width) > (item.rect.x + item.rect.width)
		and selRect.y > item.rect.y and (selRect.y + selRect.height) < (item.rect.y + item.rect.height) or
		# TopRight
		selRect.x > item.rect.x and (selRect.x + selRect.width) < (item.rect.x + item.rect.width)
		and selRect.y < item.rect.y and (selRect.y + selRect.height) > (item.rect.y + item.rect.height) or
		# BottomRight
		selRect.x > item.rect.x and (selRect.x + selRect.width) < (item.rect.x + item.rect.width)
		and selRect.y > item.rect.y and (selRect.y + selRect.height) < (item.rect.y + item.rect.height)
	):
		return True
	else: return False

# Handling item collision
def itemCollision(item, it):
	if(	item.rect.x <= (it.rect.x + it.rect.width)
		and it.rect.x 	<= (item.rect.x + item.rect.width)
		and item.rect.y <= (it.rect.y + it.rect.height)
		and it.rect.y 	<= (item.rect.y + item.rect.height)):
		return True
	else: return False

# Handling item attack collision
def attackCollision(item, it):
	if(	item.rect.x - item.sight <= (it.rect.x + it.rect.width)
		and it.rect.x - item.sight <= (item.rect.x + item.rect.width)
		and item.rect.y - item.sight <= (it.rect.y + it.rect.height)
		and it.rect.y - item.sight <= (item.rect.y + item.rect.height)):
		return True
	else: return False

# Handling fog collision
def fogCollision(item, i, j, x, y):
	if(item.rect.x - item.sight <= (i + x) and i - item.sight <= (item.rect.x + item.rect.width)
		and item.rect.y - item.sight <= (j + y) and j - item.sight <= (item.rect.y + item.rect.height)):
		return True;
	else: return False;
