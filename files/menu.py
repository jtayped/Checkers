import pygame, sys
from .settings import *

class Menu:
    def __init__(self, screen, clock) -> None:
        self.screen = screen
        self.clock = clock
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        self.drawTitles()

    def update(self):
        self.events()

        self.draw()

        pygame.display.flip()
        self.clock(FPS)