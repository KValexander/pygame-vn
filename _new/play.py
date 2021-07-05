# Connection libraries
import pygame
import os

# Connecting files
from settings import *
from common import *

# Play class
class Play:
	def __init__(self, folder):
		# Path to the project
		self.folder = folder

		# Script files data variables
		self.options = []
		self.scripts = []
		self.screens = []

	# Retrieving script files data
	def gettingFilesData():
		pass
