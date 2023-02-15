import pygame
from ..misc.settings import *
from ..misc.util import calculatePos

class Piece:
    def __init__(self, screen, row, col, playerColor) -> None:
        self.screen = screen
        self.row, self.col = row, col
        self.color = playerColor

        self.king = False

        self.radius = sqSize*0.8//2
        self.crown = pygame.image.load('files/assets/crown.png')
        self.crown = pygame.transform.scale(self.crown, (self.radius, self.radius))

        if self.color == player1Color:
            self.direction = 1
        else:
            self.direction = -1

    def __repr__(self) -> str:
        return self.color

    def makeKing(self):
        self.king = True
    
    def move(self, row, col):
        self.row, self.col = row, col

    def draw(self):
        x, y = calculatePos(self.row, self.col)
        pygame.draw.circle(self.screen, self.color, (x, y), self.radius)
        if self.king:
            x, y = calculatePos(self.row, self.col)
            self.screen.blit(self.crown, (x-self.radius, y-self.radius))

    def update(self):
        self.draw()