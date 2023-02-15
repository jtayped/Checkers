import pygame, sys
from .settings import *
from .util import drawSquares

class Menu:
    def __init__(self, screen, clock) -> None:
        self.screen = screen
        self.clock = clock

        self.player = None
        self.menu = pygame.transform.scale(pygame.image.load('files/assets/menu.png'), (WIDTH, HEIGHT))

        self.continueToGame = False
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def getMode(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            self.player = False
        elif key[pygame.K_p]:
            self.player = True

    def draw(self):
        self.screen.blit(self.menu, (0, 0))

    def update(self):
        self.events()

        self.getMode()
        self.draw()

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        self.__init__(self.screen, self.clock)
        while not self.continueToGame:
            if self.player != None:
                return self.player
            self.update()