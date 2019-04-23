import pygame, sys
from Bacteria import Bacteria
from pygame.locals import *
import random

pygame.init()
pygame.display.set_caption("Simulacion bacterias")

window = pygame.display.set_mode((700, 700))

bacterias = [Bacteria(random.randint(50, 650), random.randint(50, 650)) for i in range(random.randint(30, 50))]

clock = pygame.time.Clock()

def simulation():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        window.fill((255, 255, 255))
        for bacteria in bacterias:
            bacteria.colocar_bacteria(window)
            bacteria.movimiento()
            bacteria.update()
        clock.tick(5)
        pygame.display.flip()

if __name__ == '__main__': simulation()
