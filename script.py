# Подключение библиотек
import pygame
import codecs
import sys

# Класс работы со скриптом
class Script:
	# Инициализация класса при создании экземпляра
	def __init__(self, s):
		# Размеры экрана
		self.w, self.h = pygame.display.get_surface().get_size()
		# Переменная экрана
		self.screen = s

		# Вызов методов
		self.parse_script() # разбор скрипта
		self.init_variables() # переменные
		self.dilog_surface() # создание поверхности для диалогового окна

	# Метод инициализации переменных
	def init_variables(self):
		# Переменные текста
		self.size = 20 # размер текста
		self.color = (0,0,0) # цвет текста
		self.font = pygame.font.SysFont("verdana", self.size) # шрифт текста
		self.location = (20, self.h - self.h / 4 + 20) # отступы от краёв для текста

		# Перемеменные для подсчёт линий
		self.current_start = 0 # начало отсчёта линий скрипта
		self.current_end = len(self.lines) # окончание отсчёта линий скрипта

		# Переменные состояний
		self.hide = False # состояние отображения текста
		self.screen_state = False # состояние экрана
		self.back = False # состояние движения скрипта назад
		self.s_play = False # состояние проигрывания музыки
			
		# Переменные для диалогового окна
		self.d_width = self.w # ширина диалогового окна
		self.d_height = self.h / 4 # высота диалогового окна
		self.d_x = 0 # координата начала по горизонтали диалогового окна
		self.d_y = self.h - self.d_height # координата начала по вертикали диалогового окна
		self.d_location = (self.d_x, self.d_y) # координаты начала
		self.d_color = (255,255,255) # цвет диалогового окна

		# Стандартное изображение заднего фона
		self.bg = pygame.image.load("assets/images/defolt_bg.jpg")

	# Метод разбора файла скрипта
	def parse_script(self):
		# Получение файла скрипта
		script = codecs.open('scripts/script.vn', 'r', 'utf-8')
		# Получение текста скрипта
		text = script.read()
		
		# Разделение скрипта на область переменных и текста
		define = text.split('dialog start:')

		# Запись области переменных
		variables = define[0].split(";")
		
		# Запись области текста и команд
		self.lines = define[1].split(";")

		# Очистка линий скрипта от не нужных символов
		self.line_processing()

	# Метод очистки линий скрипта от не нужных символов
	def line_processing(self):
		# Список элементов на удаление из текста
		bad_chars = ['\r', '\n', '\t']
		# Счётчик для элементов массива
		l = 0
		# Цикл перебора линий скрипта
		while True:
			# Проверка на прерывание цикла
			if l >= len(self.lines):
				break
			# Цикл очистки текущей линии скрипта
			for i in bad_chars:
				self.lines[l] = self.lines[l].replace(i, "")
			# Увеличение счётчика
			l += 1

	# Метод обработки разделения текста и команд скрипта
	def script_processing(self):
		# Текущая линия
		self.replica = self.lines[self.current_start]
		print(self.replica)

		# Если текущая линия начинается с метки текста
		if(self.replica[0] == "\"" or self.replica[0] == "\'"):
			# Форматирование текста от кавычек
			self.replica = self.remove_char(self.replica)
			# Перезапись линии скрипта
			self.text_line()
		# Иначе
		else:
			# !!! ПЕРЕДВИЖЕНИЕ ЛИНИИ СКРИПТА НАЗАД ДОДЕЛАТЬ !!!
			# Если движение линии назад включено
			if(self.back == True):
				# Если текущая линия начинается с метки текста
				if(self.replica[0] == "\"" or self.replica[0] == "\'"):
					# Останавливаем движение назад
					self.back = False
					# Перезаписываем текущую линию
					self.text_line()
				else:
					# Вызов метода обработки команд скрипта
					self.command_processing()
			else:
				# Вызов метода обработки команд скрипта
				self.command_processing()

	# Метод обработки команд скрипта
	def command_processing(self):
		# Проверка на комментарии
		if(self.replica[0] == "#"):
			return self.current_line()

		# Проверка на команду bg
		if(self.replica.__contains__("bg")):
			# Разделение строки на команду и путь
			path = self.replica.split(" ")
			# Загрузка изображения из пути
			self.bg = pygame.image.load("assets/images/" + self.remove_char(path[1]))

		# Проврка на команду sound
		if(self.replica.__contains__("sound")):
			# Разделение строки на команду и путь
			path = self.replica.split(" ")
			# Включение состояния проигрывания музыки
			self.s_play = True
			# Загрузка музыки
			self.sound = pygame.mixer.Sound("assets/sound/" + self.remove_char(path[1]))

		# Вызов метода перехода к следующей линии скрипта
		self.current_line()

	# Метод передвижения линии скрипта
	def current_line(self):
		# Если движение назад включено
		if (self.back == True):
			# Движение диалога назад
			self.current_start -= 1
			# Отключаем движение назад
			# self.back = False
		# Иначе
		else:
			# Движение диалога вперёд
			self.current_start += 1

		# Проверка на возврат к первой линии
		if(self.current_start < 0):
			self.current_start = 0
			self.back = False

		# Проверка на окончание линий
		if(self.current_start >= self.current_end - 1):
			pygame.quit()
			sys.exit()

		# Обработка текущих линий скрипта
		self.script_processing()

	# Метод записи текущей линии скрипта
	def text_line(self):
		# Текст линии скрипта
		self.text = self.font.render(str(self.replica), True, self.color)

	# Метод создания области диалога с настройкой параметров
	def dilog_surface(self):
		# Область поверхности
		self.dialog_box = pygame.Surface((self.d_width, self.d_height))
		# Прозрачность поверхности
		self.dialog_box.set_alpha(128)
		# Цвет поверхности
		self.dialog_box.fill(self.d_color)

	# Метод обработки событий нажатий на клавиши
	def keydown(self, e):
		if e.key == pygame.K_e:
			self.display()
		if e.key == pygame.K_r:
			self.current_line() # Метод перехода к следующей линии скрипта

	# Метод обработки событий нажатий на мышь
	def mousebuttondown(self, e):
		# Если состояние экрана включено
		if(self.screen_state):
			# Если диалог не скрыт
			if self.hide == False:
				# Левая кнопка мыши
				if e.button == 1:
					self.current_line() # Вызов метода перехода к следующей линии скрипта
				# Движение колёсика мыши вперёд
				if e.button == 4:
					self.back = True # Говорим, что будет движение назад
					self.current_line() # Вызов метода перехода к следующей линии скрипта
				# Движение колёсика мыши назад
				if e.button == 5:
					self.current_line() # Вызов метода перехода к следующей линии скрипта

			# Правая кнопка мыши
			if e.button == 3:
				self.display()

		# Если состояния экрана не включено, то включить его и обработку линий
		if(self.screen_state == False):
			# Включение состояния экрана
			self.screen_state = True
			# Вызов метода обработки линий скрипта
			# Чтобы скрипт обрабатывался только при переходе на экран игры
			self.script_processing()

	# Вывод текущей линии скрипта
	def update(self):
		# Отображение заднего фона
		# self.screen.blit(self.bg, [0,0])
		self.gradual_background(self.bg)

		# Если музыка включена
		if (self.s_play == True):
			# Включение проигрывания музыки
			self.sound.play()
			# Отключение дальнейшего повторение проигрывания
			self.s_play = False

		# Если диалог не скрыт
		if self.hide == False:
			# Отображение поверхности диалогового окна
			self.screen.blit(self.dialog_box, self.d_location)
			# Отображение текста скрипта
			self.screen.blit(self.text, self.location)

	# Дополнительный метод постепенного отображения background
	def gradual_background(self, b):
		alpha = 0
		self.screen.blit(b, [0,0])

	# Дополнительный метод, убирающий первый и последний символы строки
	def remove_char(self, s):
		result = s[1 : -1]
		return result

	# Дополнительный метод изменения состояния отображения элементов экрана игры
	def display(self):
		if self.hide: self.hide = False
		else: self.hide = True