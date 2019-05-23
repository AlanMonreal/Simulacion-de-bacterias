from Bacteria import Bacteria
from pygame.locals import *
import tkinter as tk
from tkinter import *
import pygame, sys
import random
import os
import csv
import plot
import pdf_maker


clock = pygame.time.Clock()
paused = False
startcount = 0
curBact = None
bacterias = [0, 1, 2, 3, 4, 5]
sizeMin = [5, 14, 18, 20, 9, 15]
sizeMax = [15, 25, 27, 30, 23, 30]
metMin = [1, 3, 2, 4, 2, 1]
metMax = [9, 10, 12, 8, 7, 10]
initalFood = None
dictBact = {0 : "S. pneumoniae", 1 : "H. influenzae", 2 : "M. pneumoniae", 3 : "S. pyogenes", 4 : "E. coli", 5: "P. mirabilis"}
dictGram = {0 : True, 1 : False, 2 : True, 3 : True, 4 : False, 5 : False}


def start():
    global startcount, initalFood
    print(' '+ str(temp.get()) +  str(acidity.get()) + str(nutrient.get()) + str(humidity.get()))
    if curBact == None:
    	print('no bacteria selected')
    	return
    if temp.get() == 0 and acidity.get() == 0 and nutrient.get() ==0 and humidity.get() == 0:
    	return
    if startcount == 0:
        startcount += 1	
        start_button.place_forget()
        initalFood = nutrient.get() * 100000
        simulation()

def restart():
	global initalFood
	if startcount == 1:
		initalFood = nutrient.get() * 100000
		simulation()

def pause():
    global paused
    if pause_button.cget('text') == 'Pausar':
        pause_button.config(text="Resumir")
        paused = True
        return
    if pause_button.cget('text') == 'Resumir':
        pause_button.config(text="Pausar")
        paused = False
        return

def setSelectedBacteria(index):
	print('setting bacteria: ' + str(index))
	global curBact
	curBact = bacterias[index]
	sel_bact_label = Label(root, text="Bacteria seleccionada: " + dictBact[curBact], font=("Helvetica", 12))
	sel_bact_label.place(x=525, y=300)

def initiateBacteria():
	#args: curBact, sprite, tama;o Min, tama;o Max, posx, posy, gram, energia, metabolismoMin, metabolismoMax, %adaptacion, adaptacion, 
	#consumo de energia
	bacterias = [Bacteria(curBact, None, sizeMin[curBact], sizeMax[curBact],random.randint(100, 400), random.randint(100, 400), 
    	dictGram[curBact], None, metMin[curBact], metMax[curBact], None, None, None) for i in range(random.randint(20, 50))]
	return bacterias
    

def save_image():
	pygame.image.save(screen, 'current.jpeg')


def open_image():
	os.startfile('current.jpeg')


def open_pdf():
	os.startfile('simulador.pdf')


def simulation():
	global initalFood
	open_pdf_button = Button(root, text="Abrir Reporte", command=open_pdf)
	open_pdf_button.place_forget()

	initial_temp = temp.get()
	initial_acidity = acidity.get()
	initial_nutrient = nutrient.get() * 100000
	initial_humidity = humidity.get()

	bacterias = initiateBacteria()

	num_bacterias = tk.IntVar()
	bacterias_count = Label(root, text="Numero de Bacterias: ", font=("Helvetica", 12))
	bacterias_live_count = Label(root, textvariable=num_bacterias, font=("Helvetica", 12))
	bacterias_count.place(x=525, y=325)
	bacterias_live_count.place(x=680, y=325)
	start_time = pygame.time.get_ticks()
	milliseconds_paused = 0
	sim_done = False
	initalfood_zero = True
	first_frame = True
	number_of_bacterias_max = 0
	pygame.image.save(screen, "initialbacteria.jpeg")

	with open('simulador.csv', 'w+', newline='') as csvfile:
		filewrite = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewrite.writerow(['"seconds"', '"count"','"foodquant"' ])

	while True:
		if not paused:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			screen.fill((255, 255, 255))
			screen.blit(bg, (0, 0))
			nuevas_bacterias = []
			for bacteria in reversed(bacterias):
				#movimiento
				bacteria.colocar_bacteria(screen)
				bacteria.movimiento()

				#adaptacion
				bacteria.establecer_adaptacion()

				#sentidos
				bacteria.termorecepcion(temp.get())
				bacteria.sensacion_de_acidez(acidity.get())
				bacteria.sensacion_de_humedad(humidity.get())

				#energia y salud
				bacteria.ing_nut(initalFood, len(bacterias))
				#bacteria.ingerir_nutrientes(nutrient.get())
				bacteria.verificar_salud()

				#verificar si se reproduce o muere
				if bacteria.verificar_reproduccion():
					x, y = bacteria.cordenadas()
					nuevas_bacterias.append(Bacteria(curBact, None, sizeMin[curBact], sizeMax[curBact],x + random.choice([-10, 10]), 
						y + random.choice([-10, 10]), dictGram[curBact], None, metMin[curBact], metMax[curBact], None, None, None))
				if bacteria.verificar_energia() <= 0 or bacteria.verificar_salud() <= 0:
					bacterias.remove(bacteria)
					del bacteria

			bacterias = bacterias + nuevas_bacterias
			number_of_bacterias = len(bacterias)
			num_bacterias.set(number_of_bacterias)
			
			initalFood -= 1 * number_of_bacterias
			print('food left: ' + str(initalFood))

			if start_time:
				milliseconds = pygame.time.get_ticks() - start_time - milliseconds_paused
				seconds = int((milliseconds) / 1000)
			
			if number_of_bacterias > 0:
				sim_done = False
				with open('simulador.csv', 'a+', newline='') as csvfile:
					filewrite = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
					filewrite.writerow([seconds, number_of_bacterias, initalFood])

			if number_of_bacterias > number_of_bacterias_max:
				number_of_bacterias_max = number_of_bacterias
				pygame.image.save(screen, "maxbacteria.jpeg")
				print("-----------------")
					
			if number_of_bacterias == 0:
				if sim_done:
					plot.timeseries()					
					pdf_maker.make_pdf(dictBact[curBact], seconds, initial_temp, initial_acidity, initial_nutrient, initial_humidity)
					open_pdf_button.place(x=880, y=460)
					
				else:
					sim_done = True

			if first_frame:
				pygame.image.save(screen, "initialbacteria.jpeg")
				first_frame = False


		else:
			milliseconds_paused += clock.get_time()

		clock.tick(10)
		root.update()
		pygame.display.update()

root = tk.Tk()
root.title("Simulador de bacterias")
# creates embed frame for pygame window
embed = tk.Frame(root, width=900, height=500)
embed.grid(columnspan=(600), rowspan=500)  # Adds grid
embed.pack(side=LEFT)  # packs window to the left
buttonwin = tk.Frame(root, width=75, height=500)
buttonwin.pack(side=LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((500, 500))
screen.fill(pygame.Color(255, 255, 255))
pygame.display.init()
pygame.display.update()

filename = PhotoImage(file = "background.png")
background_label = Label(root, image=filename)
background_label.place(x=500, y=0)

bg = pygame.image.load("lent.png")
screen.blit(bg, (0, 0))

temp = tk.DoubleVar()
temp.set(36.5)
temp_scale = Scale(root, from_=40.0, to=33, variable=temp, length=260, resolution=0.1)
temp_label = Label(root, text="Temperatura", font=("Helvetica", 11))
temp_scale.place(x=680, y=40)
temp_label.place(x=645, y=15)

acidity = tk.DoubleVar()
acidity.set(7.4)
acidity_scale = Scale(root, from_=8, to=7.2, variable=acidity, length=260, resolution=0.001)
acidity_label = Label(root, text="Acidez", font=("Helvetica", 11))
acidity_scale.place(x=740, y=40)
acidity_label.place(x=740, y=15)

nutrient = tk.IntVar()
nutrient.set(4)
nutrient_scale = Scale(root, from_=10, to=4, variable=nutrient, length=260)
nutrient_label = Label(root, text="Nutriente", font=("Helvetica", 11))
nutrient_scale.place(x=800, y=40)
nutrient_label.place(x=795, y=15)

humidity = tk.IntVar()
humidity.set(80)
humidity_scale = Scale(root, from_=100, to=65, variable=humidity, length=260)
humidity_label = Label(root, text="Humedad", font=("Helvetica", 11))
humidity_scale.place(x=860, y=40)
humidity_label.place(x=860, y=15)

temp_label = Label(root, text="Temperatura: ", font=("Helvetica", 12))
acidity_label = Label(root, text="Acidez: ", font=("Helvetica", 12))
nutrient_label = Label(root, text="Nutriente: ", font=("Helvetica", 12))
humidity_label = Label(root, text="Humedad: ", font=("Helvetica", 12))
temp_live_label = Label(root, textvariable=temp, font=("Helvetica", 12))
acidity_live_label = Label(root, textvariable=acidity, font=("Helvetica", 12))
nutrient_live_label = Label(root, textvariable=nutrient, font=("Helvetica", 12))
humidity_live_label = Label(root, textvariable=humidity, font=("Helvetica", 12))
temp_label.place(x=525, y=350)
acidity_label.place(x=525, y=375)
nutrient_label.place(x=525, y=400)
humidity_label.place(x=525, y=425)
temp_live_label.place(x=620, y=350)
acidity_live_label.place(x=583, y=375)
nutrient_live_label.place(x=600, y=400)
humidity_live_label.place(x=605, y=425)

bacteria_label = Label(root, text="Bacteria", font=("Helvetica", 20))
bacteria_1 = Button(root, text="S. pneumoniae", command=lambda:setSelectedBacteria(0))
bacteria_2 = Button(root, text="H. influenzae", command=lambda: setSelectedBacteria(1))
bacteria_3 = Button(root, text="M. pneumoniae", command=lambda: setSelectedBacteria(2))
bacteria_4 = Button(root, text="S. pyogenes", command=lambda:setSelectedBacteria(3))
bacteria_5 = Button(root, text="E. coli", command=lambda: setSelectedBacteria(4))
bacteria_6 = Button(root, text="P. mirabilis", command=lambda: setSelectedBacteria(5))
bacteria_label.place(x=520, y=35)
bacteria_1.place(x=535, y=75)
bacteria_2.place(x=535, y=105)
bacteria_3.place(x=535, y=135)
bacteria_4.place(x=535, y=165)
bacteria_5.place(x=535, y=195)
bacteria_6.place(x=535, y=225)

sel_bact_label = Label(root, text="Bacteria seleccionada: ", font=("Helvetica", 12))
sel_bact_label.place(x=525, y=300)


start_button = Button(root, text="Empezar", command=start)
pause_button = Button(root, text="Pausar", command=pause)
restart_button = Button(root, text="Reiniciar", command=restart)
start_button.place(x=780, y=350)
pause_button.place(x=755, y=390)
restart_button.place(x=810, y=390)

save_image_button = Button(root, text="Guardar imagen", command=save_image)
save_image_button.place(x=525, y=460)
open_image_button = Button(root, text="Ver imagen", command=open_image)
open_image_button.place(x=625, y=460)


while True:
    pygame.display.update()
    root.update()
