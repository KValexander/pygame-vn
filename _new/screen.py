# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *

# Class option
class Screen:
	def __init__(self, window, config, data):
		self.window = window
		self.config = config
		self.data 	= data