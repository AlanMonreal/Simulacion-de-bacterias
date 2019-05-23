import pygame, sys
from pygame.locals import *
import random

class Bacteria(pygame.sprite.Sprite):
	def __init__(self, bacteria ,sprite, tamanoMin, tamanoMax, position_x, position_y, gram, energia, metabolismoMin, 
		metabolismoMax, porcentage_de_adaptacion, adaptacion, consumo_de_energia):
		""" posicion de la bacteria en la simulacion
			gram: definir si la bacteria es gram positiva:True o negativa:False"""
		pygame.sprite.Sprite.__init__(self)

		#sprite de la bacteria
		self.sprite = pygame.image.load(sprite) if sprite else pygame.image.load("sprites/bacteria.png")
		self.tamano = random.randint(tamanoMin,tamanoMax) if tamanoMin and tamanoMax else random.randint(10,30) #checar el tama;o
		self.sprite = pygame.transform.scale(self.sprite, (self.tamano, self.tamano))
		self.sprite_de_bacteria = self.sprite.get_rect()

		#variables de la bacteria
		self.bacteria = bacteria if bacteria else 0
		self.sprite_de_bacteria.centerx = position_x
		self.sprite_de_bacteria.centery = position_y
		self.gram = gram if gram else True
		self.salud = 100
		self.energia = energia if energia else random.randint(0, 100)
		self.reproduccion = False
		self.pared_celular = 100 if self.gram else 20
		self.metabolismo = random.randint(metabolismoMin, metabolismoMax) / 10 if metabolismoMin and metabolismoMax else random.randint(1, 9) / 10 
		self.porcentage_de_adaptacion = porcentage_de_adaptacion if porcentage_de_adaptacion else random.randint(1, 5) / 10
		self.adaptacion = adaptacion if adaptacion else 0.0
		self.tiempo = 0
		self.consumo_de_energia = consumo_de_energia if consumo_de_energia else (random.randint(3, 6) / 10) * -1


		self.sPneumonieaTemp = [15, 25, 34, 36, 40, 45]
		self.sPneumonieaPh = [7.4, 7.8, 7.3, 7.2, 7.9, 8]
		sPneumonieaHum = []

		self.influenzaeTemp = [20, 26, 35, 36.9, 38, 40]
		self.influenzaePh = [7.55, 7.65, 7.43, 7.2, 7.75, 8]
		influenzaeHum = []

		self.mPneumonieaTemp = [25, 33, 36.7, 37.5, 38.7, 39]
		self.mPneumonieaPh = [7.73, 8, 7.6, 7.2, 8.2, 10]
		mPneumonieaHum = []

		self.pyogenesTemp = [25, 30, 36, 37.5, 39, 45]
		self.pyogenesPh = [7.73, 8, 7.58, 7.23, 8.2, 10]
		pyogenesHum = []

		self.coliTemp = [20, 30, 35, 38, 40, 46]
		self.coliPh = [6.5, 7.2, 6, 4, 7.65, 8]
		coliHum = []

		self.mirabilisTemp = [25, 33, 36.7, 37.5, 38.7, 39]
		self.mirabilisPh = [7.7, 8, 7,4, 6.5, 9.8, 12]
		mirabilisHum = []

		self.temp = [self.sPneumonieaTemp, self.influenzaeTemp, self.mPneumonieaTemp, self.pyogenesTemp, self.coliTemp, self.mirabilisTemp]
		self.pH = [self.sPneumonieaPh, self.influenzaePh, self.mPneumonieaPh, self.pyogenesPh, self.coliPh, self.mirabilisPh]
		#self.humidity = [self.sPneumonieaHum, self.influenzaeHum, self.mPneumonieaHum, self.pyogenesHum, self.coliHum, self.mirabilisHum]



	def termorecepcion(self, temperatura):
		if temperatura < self.temp[self.bacteria][0]:
			self.salud -= 10
		elif temperatura > self.temp[self.bacteria][0] and temperatura < self.temp[self.bacteria][1]:
			self.salud -= 0.5
		elif temperatura > self.temp[self.bacteria][1] and temperatura < self.temp[self.bacteria][2]:
			self.salud -= 0.1
		elif temperatura > self.temp[self.bacteria][2] and temperatura < self.temp[self.bacteria][3]:
			self.salud = self.salud
		elif temperatura > self.temp[self.bacteria][3] and temperatura < self.temp[self.bacteria][4]:
			self.salud -= 0.1
		elif temperatura > self.temp[self.bacteria][4] and temperatura < self.temp[self.bacteria][5]:
			self.salud -= 0.5
		elif temperatura > self.temp[self.bacteria][5]: 
			self.salud -= 10

	def sensacion_de_humedad(self, porcentage):
		if porcentage >= 0 and porcentage <= 20:
			self.salud -= 2
		elif porcentage > 20 and porcentage <= 40: 
			self.salud -= 1
		elif porcentage > 40 and porcentage <= 60 and self.salud <= 100: 
			self.salud += 0.01
		elif porcentage > 60 and porcentage <= 80 and self.salud <= 100: 
			self.salud += 0.1
		elif porcentage > 80 and porcentage <= 100 and self.salud <= 100: 
			self.salud += 0.2

	def sensacion_de_acidez(self, pH):
		#pH 7 es neutro, < es acido, > 7 es base
		if pH > self.pH[self.bacteria][0] and pH < self.pH[self.bacteria][1]:
			self.salud = self.salud
		elif pH > self.pH[self.bacteria][2] and pH < self.pH[self.bacteria][0]:
			self.salud -= 0.3 
		elif pH > self.pH[self.bacteria][3] and pH < self.pH[self.bacteria][2]:
			self.salud -= 0.5
		elif pH > self.pH[self.bacteria][1] and pH < self.pH[self.bacteria][4]:
			self.salud -= 0.3
		elif pH > self.pH[self.bacteria][4] and pH < self.pH[self.bacteria][5]:
			self.salud -= 0.5
		elif pH < self.pH[self.bacteria][3]:
			self.salud -= 0.75
		elif pH > self.pH[self.bacteria][5]:
			self.salud -= 0.75

	def ingerir_nutrientes(self, nutrinte):
		if self.energia < 100:
			self.energia += nutrinte * self.metabolismo
		elif self.energia > 100: 
			self.energia = 90

	def ing_nut(self, nutriente, cantBact):
		if(nutriente > (cantBact * 3)):
			nut = 3
		elif(nutriente > (cantBact * 2)):
			nut = 2
		elif(nutriente < 0):
			nut = 0
			self.salud -= 0.2
		else:
			nut = 1
			self.salud -= 0.01
		if self.energia < 100 and nut != 0:
			self.energia += nut * self.metabolismo
		elif self.energia > 100: 
			self.energia = 90

	def receptor_de_antibiotico(self, daño):
		pass

	def verificar_reproduccion(self):
		if self.energia > 95 and self.energia < 100 and self.adaptacion > 90:
			self.energia -= 50
			return True
		else: return False

	def verificar_energia(self):
		self.energia += self.consumo_de_energia - 0.1
		return self.energia
	
	def verificar_salud(self):
		return self.salud

	def establecer_adaptacion(self):
		self.adaptacion += self.porcentage_de_adaptacion 

	def colocar_bacteria(self, window):
		window.blit(self.sprite, self.sprite_de_bacteria)

	def cordenadas(self):
		return self.sprite_de_bacteria.centerx, self.sprite_de_bacteria.centery

	def movimiento(self):
		self.sprite_de_bacteria.centerx += random.randint(-1, 1) 
		self.sprite_de_bacteria.centery += random.randint(-1, 1)
