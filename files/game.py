import pygame
from .settings import *
from .elements.board import Board

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

        # pvp = Player vs Player // pvc = Player vs Computer
        self.modes = ['pvp', 'pvc']

    def run(self):
        Board(self.screen, self.clock, self.modes[0]).run()