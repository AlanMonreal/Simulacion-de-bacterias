import pygame, sys

from pygame.locals import *

pygame.init()
pygame.display.set_caption("Simulacion bacterias")

window = pygame.display.set_mode((1200, 700))

def simulation():
    while True:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
if __name__ == '__main__':
    simulation()
