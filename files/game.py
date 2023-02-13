import pygame
from .settings import *
from .elements.board import Board

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        self.winnerFont = pygame.font.Font("files/fonts/Cinzel-Bold.ttf", 75)

        # pvp = Player vs Player // pvc = Player vs Computer
        self.modes = ['pvp', 'pvc']

    def run(self):
        Board(self.screen, self.clock, self.modes[0], self.winnerFont).run()