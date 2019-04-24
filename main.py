from Bacteria import Bacteria
from pygame.locals import *
import tkinter as tk
from tkinter import *
import pygame, sys
import random
import os


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

bg = pygame.image.load("sim_background.png")
screen.blit(bg, (0, 0))

time = tk.IntVar()
time.set(0)
time_scale = Scale(root, from_=0, to=200, variable=time, length=260)
time_label = Label(root, text="Tiempo", font=("Helvetica", 11))
time_scale.place(x=680, y=40)
time_label.place(x=680, y=15)

acidity = tk.IntVar()
acidity.set(0)
acidity_scale = Scale(root, from_=0, to=200, variable=acidity, length=260)
acidity_label = Label(root, text="Acidez", font=("Helvetica", 11))
acidity_scale.place(x=740, y=40)
acidity_label.place(x=740, y=15)

nutrient = tk.IntVar()
nutrient.set(0)
nutrient_scale = Scale(root, from_=0, to=200, variable=nutrient, length=260)
nutrient_label = Label(root, text="Nutriente", font=("Helvetica", 11))
nutrient_scale.place(x=800, y=40)
nutrient_label.place(x=795, y=15)

humidity = tk.IntVar()
humidity.set(0)
humidity_scale = Scale(root, from_=0, to=200, variable=humidity, length=260)
humidity_label = Label(root, text="Humedad", font=("Helvetica", 11))
humidity_scale.place(x=860, y=40)
humidity_label.place(x=860, y=15)

tiempo_label = Label(root, text="Tiempo: ", font=("Helvetica", 12))
acidity_label = Label(root, text="Acidez: ", font=("Helvetica", 12))
nutrient_label = Label(root, text="Nutriente: ", font=("Helvetica", 12))
humidity_label = Label(root, text="Humedad: ", font=("Helvetica", 12))
tiempo_live_label = Label(root, textvariable=time, font=("Helvetica", 12))
acidity_live_label = Label(root, textvariable=acidity, font=("Helvetica", 12))
nutrient_live_label = Label(
    root, textvariable=nutrient, font=("Helvetica", 12))
humidity_live_label = Label(
    root, textvariable=humidity, font=("Helvetica", 12))
tiempo_label.place(x=525, y=350)
acidity_label.place(x=525, y=375)
nutrient_label.place(x=525, y=400)
humidity_label.place(x=525, y=425)
tiempo_live_label.place(x=590, y=350)
acidity_live_label.place(x=583, y=375)
nutrient_live_label.place(x=600, y=400)
humidity_live_label.place(x=605, y=425)


antibiotic_label = Label(root, text="Antibiotico", font=("Helvetica", 20))
antibiotic_label.place(x=520, y=35)
antibiotic_1 = Button(root, text="lorem ipsum", command=quit)
antibiotic_1.place(x=545, y=75)
antibiotic_2 = Button(root, text="lorem ipsum", command=quit)
antibiotic_2.place(x=545, y=105)
antibiotic_3 = Button(root, text="lorem ipsum", command=quit)
antibiotic_3.place(x=545, y=135)


bacteria_label = Label(root, text="Bacteria", font=("Helvetica", 20))
bacteria_label.place(x=530, y=165)
bacteria_1 = Button(root, text="lorem ipsum", command=quit)
bacteria_1.place(x=545, y=205)
bacteria_2 = Button(root, text="lorem ipsum", command=quit)
bacteria_2.place(x=545, y=235)
bacteria_3 = Button(root, text="lorem ipsum", command=quit)
bacteria_3.place(x=545, y=265)

start = Button(root, text="Empezar", command=quit)
pause = Button(root, text="Pausar", command=quit)
restart = Button(root, text="Reiniciar", command=quit)
start.place(x=730, y=350)
pause.place(x=810, y=350)
restart.place(x=770, y=390)



clock = pygame.time.Clock()

bg = pygame.image.load("sim_background.png")
def simulation():
    bacterias = [Bacteria(random.randint(100, 400), random.randint(100, 400))
                for i in range(random.randint(20, 50))]
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        nuevas_bacterias = []

        for bacteria in bacterias:
            bacteria.colocar_bacteria(screen)
            bacteria.movimiento()
            bacteria.establecer_tiempo()
            bacteria.ingerir_nutrientes(2)
            if bacteria.verificar_reproduccion():
                x, y = bacteria.cordenadas()
                nuevas_bacterias.append(Bacteria(x + random.randint(-10, 10), y + random.randint(-10, 10)))
        bacterias = bacterias + nuevas_bacterias
        print(len(bacterias))
        root.update()
        clock.tick(10)
        pygame.display.update()

if __name__ == '__main__': simulation()
