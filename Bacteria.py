import pygame, sys
from pygame.locals import *
import random

class Bacteria(pygame.sprite.Sprite):
	def __init__(self, position_x, position_y, gram=True):
		""" posicion de la bacteria en la simulacion
			gram: definir si la bacteria es gram positiva:True o negativa:False"""
		pygame.sprite.Sprite.__init__(self)

		#sprite de la bacteria
		self.sprite = pygame.image.load("sprites/bacteria.png")
		self.sprite_de_bacteria = self.sprite.get_rect()

		#posicion de la bacteria
		self.sprite_de_bacteria.centerx = position_x
		self.sprite_de_bacteria.centery = position_y
		self.gram = gram
		self.salud = 100
		self.energia = 100
		self.reproduccion = False

	def colocar_bacteria(self, window):
		window.blit(self.sprite, self.sprite_de_bacteria)