import random
from ..settings import *

class Computer:
    def __init__(self) -> None:
        pass

    def getMove(self, board):
        options = []
        for indexRow,row in enumerate(board):
            for indexCol,col in enumerate(row):
                sq = board[indexRow][indexCol]
                if sq != 0 and sq.color == player2Color:
                    validMoves = sq.getValidMoves(board)
                    if len(validMoves) > 0:
                        options.append([[indexRow, indexCol], sq.getValidMoves(board)])
        
        pieceAndMove = random.choice(options)
        print(pieceAndMove)
        pieceCord = pieceAndMove[0]
        moveKill = random.choice(pieceAndMove[1])
        move = moveKill[0]
        kill = moveKill[1]
        return pieceCord, move, kill, player2Color