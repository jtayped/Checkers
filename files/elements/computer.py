from ..misc.util import *
import random

class Computer:
    def __init__(self, playerColor) -> None:
        self.playerColor = playerColor
    
    def getMove(self, board):
        pieces = getPiecesWidthValidMoves(board, self.playerColor)
        
        piece = random.choice(pieces)
        validMoves = getValidMoves(board, piece)
        move = random.choice(validMoves)
        return piece, move