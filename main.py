import pygame, sys
from Bacteria import Bacteria
from pygame.locals import *
import random

pygame.init()
pygame.display.set_caption("Simulacion bacterias")

window = pygame.display.set_mode((700, 700))


clock = pygame.time.Clock()

def simulation():
    while True:
        bacterias = [Bacteria(random.randint(0, 700), random.randint(0, 700)) for i in range(20)]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        window.fill((255, 255, 255))
        for bacteria in bacterias:
            bacteria.colocar_bacteria(window)
            bacteria.update()
        clock.tick(6)
        pygame.display.flip()

if __name__ == '__main__': simulation()
