import pygame
from ..settings import *

class Piece:
    def __init__(self, screen, row, col, color) -> None:
        self.screen = screen
        self.row, self.col = row, col
        self.color = color
        self.king = False

        if self.color == player1Color:
            self.direction = 1
        else:
            self.direction = -1

        self.x, self.y = 0, 0
        self.calculatePos()
    
    def calculatePos(self):
        self.x, self.y = sqSize*self.row + sqSize//2, sqSize*self.col + sqSize//2

    def makeKing(self):
        self.king = True
    
    def draw(self):
        radius = sqSize*0.8//2
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), radius)
    
    def update(self):
        self.draw()

    def __repr__(self) -> str:
        return self.color