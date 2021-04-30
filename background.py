# Подключение библиотек
import pygame

# Источник: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
# Класс написан не мной
# Класс позволяющий ставить на задний фон изображения в полном размере
# class Background(pygame.sprite.Sprite):
#     def __init__(self, image_file, location):
#         pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
#         self.image = pygame.image.load(image_file)
#         self.rect = self.image.get_rect()
#         self.rect.left, self.rect.top = location

# Собственно написанный класс
# Класс для отображения заднего фона
class Background:
	# Инициализация класса
	def __init__(self, s,  image_file, location):
		# Загрузка изображения
		self.image = pygame.image.load(image_file)
		# Отображение изображения
		s.blit(self.image, location)
