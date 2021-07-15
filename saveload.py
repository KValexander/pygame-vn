# Connection libraries
import pygame
import codecs
import os
import re

# Connecting files
from settings import *
from common import *

# class SaveLoad
class SaveLoad:
	def __init__(self, screen, option, main):
		self.screen = screen
		self.option = option
		self.main   = main
		self.printstate = False

	# Loading data
	def loadConfig(self, cell):
		if cell["workload"] == False: return
		self.main.processingScript()

		# Retrieving and Clearing Data 
		file = codecs.open(cell["pathToSave"], "r")
		config = file.read().split("\n")
		config = [x for x in config if x != ""]
		result = {}

		# Data parsing
		for conf in config:
			# Parsing data
			key, value = parsingLine(conf)
			value = value.replace(" ", "", 1)
			value = re.sub(r"<.*?>", "''", value)
			result[key] = {}

			# Font
			if key == "font":
				size = self.screen.config[self.screen.config["playScreen"]]["play"]["text"]["size"]
				if self.option.config["typeFont"] == "system":
					result[key] = pygame.font.SysFont(self.option.config["systemFont"], size)
				elif self.option.config["typeFont"] == "own":
					if os.path.exists(self.option.config["pathToProject"] + self.option.config["ownFont"]):
						result[key] = pygame.font.Font(self.option.config["pathToProject"] + self.option.config["ownFont"], size)
					else: result[key] = pygame.font.SysFont("calibri", size)
				else: result[key] = pygame.font.SysFont("calibri", size)

			# For objects without nesting
			singly = re.findall(r"(?:\'.*?\':\s\w+)|(?:\'.*?\':\s\'.*?\')|(?:\'.*?\':\s\(.*?\))", value)
			# For nested objects
			nested = re.findall(r"\'.*?\':\s\{.*?\}", value)
			# For max nested objects
			maxnested = re.findall(r"(\'(?:names|characters)\':\s\{(?:\'.*?\':\s\{.*?\})*\})", value)
			# For arrays of objects
			arrays = re.findall(r"\'(?:clauses)\':\s\[.*?\]", value)

			if self.printstate:
				print(f"==========={key}============")
				print(f"{key} || {value}")
				
				if key == "lines" or key == "background" or key == "bool":
					print("-----------singly------------")
					print(singly)
				elif key == "variables" or key == "render":
					print("-----------nested------------")
					print(nested)
					print("----------maxnested----------")
					print(maxnested)
					print("------------arrays-----------")
					print(arrays)
				else:
					print("-----------unclear-----------")
					print(value)
				print("")

			# Parsing variables
			if key == "variables":
				# For nested objects
				for nest in nested:
					nest = nest.split(":", 1)
					name, items = removeChar(nest[0]), removeChar(nest[1])
					items = re.sub(r"(\')|(\s)|(\{)|(\})", "", items)
					# Handling counters and booleans
					if name == "counters" or name == "booleans":
						result[key][name] = {}
						items = items.split(",")
						for item in items:
							subname, val = item.split(":")
							if name == "counters": val = int(val)
							result[key][name][subname] = val
				# For max nested objects
				for nest in maxnested:
					name, objects = nest.split(":", 1)
					name = removeChar(name)
					result[key][name] = {}
					if name == "names" or name == "characters":
						objects = re.findall(r"\'.*?\':\s\{.*?\}", objects)
						for obj in objects:
							obj = obj.split(":", 1)
							subname, items = removeChar(obj[0]), removeChar(obj[1])
							items = re.sub(r"(\')|(\s)|(\{)|(\})", "", items)
							result[key][name][subname] = {}
							items = items.split(",", 1)
							for item in items:
								undername, val = item.split(":")
								if undername == "color": val = defineColor(val)
								elif undername == "coord": val = fetchSize(val)
								result[key][name][subname][undername] = val
								
			# Parsing lines
			elif key == "lines":
				for single in singly:
					single = single.replace("'", "")
					name, val = single.split(":", 1)
					val = val.replace(" ", "", 1)
					if name == "start" or name == "end": val = int(val)
					result[key][name] = val
				result[key]["lines"] = []
				if result[key]["namekey"] != "":
					nname = result["variables"]["names"][result[key]["namekey"]]
					result[key]["name"] = result["font"].render(nname["value"], True, nname["color"])

			# Parsing background
			elif key == "background":
				for single in singly:
					single = single.replace("'", "")
					name, val = single.split(":", 1)
					val = val.replace(" ", "", 1)
					if name == "src":
						result[key][name] = val
						result[key]["image"] = scLoadImage(val, self.option.config["size"])

			# Parsing render
			elif key == "render":
				# For max nested objects
				for nest in maxnested:
					name, objects = nest.split(":", 1)
					name = removeChar(name)
					result[key][name] = {}
					if name == "characters":
						objects = re.findall(r"\'.*?\':\s\{.*?\}", objects)
						for obj in objects:
							obj = obj.split(":", 1)
							subname, items = removeChar(obj[0]), removeChar(obj[1])
							src = self.option.config["pathToCharacter"] + result["variables"]["characters"][subname]["src"]
							items = re.sub(r"(\')|(\s)|(\{)|(\})", "", items)
							result[key][name][subname] = {}
							items = items.split(",", 2)
							for item in items:
								undername, val = item.split(":")
								if undername == "coord": val = fetchSize(val)
								elif undername == "state":
									if val == "True": val = True
									elif val == "False": val = False
								elif undername == "image": val = loadImage(src)
								result[key][name][subname][undername] = val
				# For arrays of objects
				for element in arrays:
					name, array = element.split(":", 1)
					name = removeChar(name)
					result[key][name] = []
					objects = re.findall(r"{.*?}", array)
					for obj in objects:
						coords, texts = re.findall(r"\'(?:xy|wh|txy|twh)\':\s\(.*?\)", obj), re.findall(r"\'(?:text|value|return|hover)\':\s\'.*?\'", obj) 
						entity = {}
						for coord in coords:
							coord = re.sub(r"(\')|(\s)", "", coord)
							subname, val = coord.split(":", 1)
							entity[subname] = fetchSize(val)
						for text in texts:
							text = re.sub(r"(\')", "", text)
							subname, val = text.split(":", 1)
							entity[subname] = val.replace(" ", "", 1)
						entity["hover"] = False
						entity["text"] = result["font"].render(entity["value"], True, self.screen.config[self.screen.config["playScreen"]]["play"]["text"]["color"])
						result[key][name].append(entity)

			# Parsing condition
			elif key == "condition" and len(value) != 2:
				coords, texts = re.findall(r"\'(?:wh|xy|txy)\':\s\(.*?\)", value), re.findall(r"\'(?:text|value|surface)\':\s\'.*?\'", value) 
				for coord in coords:
					coord = re.sub(r"(\')|(\s)", "", coord)
					name, val = coord.split(":", 1)
					result[key][name] = fetchSize(val)
				for text in texts:
					text = re.sub(r"(\')", "", text)
					name, val = text.split(":", 1)
					result[key][name] = val.replace(" ", "", 1)
				result[key]["text"] = result["font"].render(result[key]["value"], True, self.option.config["conditionTextColor"])
				result[key]["surface"] = pygame.Surface(result[key]["wh"])
				result[key]["surface"].fill(self.option.config["conditionBackgroundColor"])
				result[key]["surface"].set_alpha(self.option.config["conditionAlpha"])

			# Parsing music
			elif key == "music":
				musics = re.sub(r"(\')|(\s)|(\{)|(\})", "", value)
				musics = musics.split(",")
				for music in musics:
					name, val = music.split(":", 1)
					result[key][name] = val
			
			# Parsing bool
			elif key == "bool":
				for single in singly:
					single = single.replace("'", "")
					name, val = single.split(":", 1)
					val = val.replace(" ", "", 1)
					if val == "True": val = True
					elif val == "False": val = False
					result[key][name] = val

		self.main.script.config = result
		self.main.script.setTextOnLine()

	# Saving data
	def saveConfig(self, cell, config):
		path = self.option.config["pathToSaves"] + cell["name"] + ".save"
		with open(path, "w") as file:
			for key, value in config.items():
				if self.printstate:
					print("=============================")
					print(f"{key} || {value}")
				file.write(f"{key} {value}\n")

		# Check cells
		if "cells" in self.main.currentScreen["elements"]:
			self.main.currentScreen["elements"]["cells"].checkCells()
		elif "cells" in self.main.currentSubscreen["elements"]:
			self.main.currentSubscreen["elements"]["cells"].checkCells()