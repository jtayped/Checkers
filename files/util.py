from .settings import *
import pygame

def calculatePos(row, col):
    return sqSize*col + sqSize//2, sqSize*row + sqSize//2

def drawSquares(screen):
    for row in range(sqInWidth):
        for col in range(row % 2, sqInWidth, 2):
            pygame.draw.rect(screen, BOARD_COLOR, (row*sqSize, col*sqSize, sqSize, sqSize))