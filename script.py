# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *

# Class option
class Script:
	def __init__(self, window, data):
		self.window = window
		self.data 	= data
		self.config = {}

	# Passing data to the main class
	def getConfig(self):
		return self.config