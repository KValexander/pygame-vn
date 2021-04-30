# Подключение библиотек
import pygame

# Подключение сторонних классов
from background import Background

# Класс работы с экраном меню
class Menu:
	# Инициализация класса при создании экземпляра
	def __init__(self, s):
		# Размеры экрана
		self.w, self.h = pygame.display.get_surface().get_size()
		# Экран игры
		self.screen = s
		# Вызов метода инициализации переменных
		self.init_variable()

	# Метод инициализации переменных
	def init_variable(self):
		# Шрифт
		self.font = pygame.font.SysFont("verdana", 20)

	# Метод создания кнопок
	def create_button(self, x, y, width, height, b_color, val, t_color):
		# Получение размеров текста
		t_w, t_h = self.font.size(val);
		# Высчитывание расположение текста на кнопке
		location = (x + width / 2 - t_w / 2, y + height / 2 - t_h / 2)
		# Задание текста
		text = self.font.render(str(val), True, t_color)
		# Создание прямоугольника
		rect = pygame.Rect(x, y, width, height)
		# Отрисовка прямоугольника
		pygame.draw.rect(self.screen, (0,0,0), rect, 0)
		# Отрисовка текста
		self.screen.blit(text, location)
		# Возвращение области кнопки
		return rect

	# Метод создания поверхностей
	def create_surface(self, xy, wh, color, transparency):
		# Область поверхности
		surface = pygame.Surface(wh)
		# Прозрачность поверхности от 0 до 255
		surface.set_alpha(transparency)
		# Заливка поверхности
		surface.fill(color)
		# Отрисовка поверхности
		self.screen.blit(surface, xy)

	# Метод обработки событий нажатий на мышь
	def mousebuttondown(self, e, l):
		# Обработка нажатия на кнопку старта игры
		if self.b_start.collidepoint(e.pos):
			# Левая кнопка мыши
			if e.button == 1:
				# Изменение экрана
				l.menu = False # меню
				l.game = True # игра
			# Правая кнопка мыши
			if e.button == 3:
				# Изменение экрана
				l.menu = False # меню
				l.game = True # игра

		# Обработка нажатия на кнопку выхода из игры
		if self.b_end.collidepoint(e.pos):
			# Левая кнопка мыши
			if e.button == 1:
				# Выход из игры
				l.main_loop = False # основной цикл
			# Правая кнопка мыши
			if e.button == 3:
				# Выход из игры
				l.main_loop = False # основной цикл

	# Метод обновления данных меню
	def update(self):
		# Изображение на задний фон
		self.bg = Background(self.screen, "assets/gui/background.jpg", [0,0])
		
		# Создание поверхностей
		# Поверхность для кнопко меню
		self.menu_surface = self.create_surface([0,0], [300, self.h], (255,255,255), 128)

		# Создание кнопок
		# Кнопка начала игры
		self.b_start = self.create_button(50, 50, 200, 50, (0,0,0), "Start game", (255,255,255))
		# Кнопка конца игры
		self.b_end = self.create_button(50, self.h - 100, 200, 50, (0,0,0), "Exit game", (255,255,255))