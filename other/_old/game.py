# Подключение библиотек
import pygame
from pygame.color import THECOLORS

# Подключение классов
from gui import Menu
from script import Script

# Класс состояний игровых циклов и экранов игры
class Loop:
	# Инициализация класса
	def __init__(self):
		# Основной игровой цикл
		self.main_loop = True
		# Экран меню
		self.menu = True
		# Экран игры
		self.game = False

# Класс игры
class Game(object):
	# Инициализация класса при создании экземпляра
	def __init__(self):
		self.init_window()
		self.init_variables()

	# Метод настроек окон игры
	def init_window(self):
		# Размеры экрана
		self.WIDTH = 1200
		self.HEIGHT = 800
		self.SIZE = (self.WIDTH, self.HEIGHT)

		# Экран
		self.screen = pygame.display.set_mode(self.SIZE)

		# Экземпляр класса с состояниями циклов и экранов игры
		self.loop = Loop()

	# Метод инициализации переменных
	def init_variables(self):
		# Переменная времени
		self.clock = pygame.time.Clock()

		# Создание экземпляров классов
		self.menu = Menu(self.screen)
		self.script = Script(self.screen)

	# Метод обработки событий
	def events(self):
		# Цикл обработки событий
		for event in pygame.event.get():
			# MOUSEBUTTONDOWN
			# 1 - нажатие левой кнопки мыши
			# 2 - нажатие колёсика мыши
			# 3 - нажатие правой кнопки мыши
			# 4 - движение колёсика вперёд
			# 5 - движение колёсика назад

			# Обработка события выхода из игры
			if event.type == pygame.QUIT:
				self.loop.main_loop = False

			# Обработка событий экрана меню
			if self.loop.menu:
				# Обработка событий нажатия на мышь
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.menu.mousebuttondown(event, self.loop)

			# Обработка событий экрана игры
			if self.loop.game:
				# Обработка событий нажатия на клавиши
				if event.type == pygame.KEYDOWN:
					self.script.keydown(event)
				# Обработка событий нажатия на мышь
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.script.mousebuttondown(event)

	# Метод обновления данных
	def update(self):
		# Вызов метода обработки событий
		self.events()

	# Метод отрисовки данных
	def render(self):
		# Рендер экрана меню
		if self.loop.menu:
			# Цвет фона
			self.screen.fill((100,100,100))

			# Методы отображения данных классов
			self.menu.update()

		# Рендер экрана игры
		if self.loop.game:
			# Цвет фона
			self.screen.fill((0,0,0))

			# Методы отображения данных классов
			self.script.update()

		# Отрисовка данных
		pygame.display.flip()
		# Количество кадров в секунду
		self.clock.tick(60)