from ..misc.util import *
import random

class Computer:
    def __init__(self, playerColor) -> None:
        self.playerColor = playerColor
    
    def eval(self, board):
        player1Pieces = player2Pieces = player1Kings = player2Kings = 0

        for rowIndex,row in enumerate(board):
            for colIndex,col in enumerate(row):
                piece = board[rowIndex][colIndex]
                if piece != 0:
                    if piece.color == player1Color:
                        player1Pieces += 1
                    elif piece.color == player2Color:
                        player2Pieces += 1

                    if piece.king:
                        if piece.color == player1Color:
                            player1Kings += 1
                        elif piece.color == player2Color:
                            player2Kings += 1

        return #eval value

    def getMove(self, board):
        pieces = getPiecesWidthValidMoves(board, self.playerColor)
        
        piece = random.choice(pieces)
        validMoves = getValidMoves(board, piece)
        move = random.choice(validMoves)
        return piece, move