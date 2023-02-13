from .settings import *

def calculatePos(row, col):
    return sqSize*col + sqSize//2, sqSize*row + sqSize//2