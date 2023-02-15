import pygame, sys
from ..misc.settings import *
from ..misc.util import *

class Menu:
    def __init__(self, screen, clock, modes) -> None:
        self.screen = screen
        self.clock = clock
        self.modes = modes

        self.mode = None
        self.menu = pygame.transform.scale(pygame.image.load('files/assets/menu.png'), (WIDTH, HEIGHT))

        self.continueToGame = False
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def getMode(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            self.mode = self.modes[1]
        elif key[pygame.K_p]:
            self.mode = self.modes[0]

    def draw(self):
        self.screen.blit(self.menu, (0, 0))

    def update(self):
        self.events()

        self.getMode()
        self.draw()

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        self.__init__(self.screen, self.clock, self.modes)
        while self.mode == None:
            self.update()
        
        return self.mode