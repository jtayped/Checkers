import pygame
from .misc.settings import *
from .screens.Board import Board
from .screens.Menu import Menu

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        self.winnerFont = pygame.font.Font("files/fonts/Cinzel-Bold.ttf", 75)
        self.subtitleFont = pygame.font.Font("files/fonts/Cinzel-Bold.ttf", 35)

        # pvp = Player vs Player // pvc = Player vs Computer
        self.modes = ['pvp', 'pvc']

        self.menu = Menu(self.screen, self.clock, self.modes)

    def run(self):
        while True:
            mode = self.menu.run()
            Board(self.screen, self.clock, mode, self.winnerFont, self.subtitleFont).run()
        pygame.quit()