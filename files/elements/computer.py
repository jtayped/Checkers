from ..misc.util import *
import random
from copy import deepcopy

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

        return player2Pieces - player1Pieces + player2Kings*2

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        if depth == 0 or checkWin(board):
            return self.eval(board)

        if maximizing_player:
            bestValue = float("-inf")
            for piece in getPiecesWidthValidMoves(board, player2Color):
                for move in getValidMoves(board, piece):
                    newBoard = deepcopy(board)
                    newBoard = makeMove(newBoard, player2Color, piece, move)
                    value = self.minimax(newBoard, depth - 1, False, alpha, beta)
                    bestValue = max(bestValue, value)
                    alpha = max(alpha, bestValue)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return bestValue
        else:
            bestValue = float("inf")
            for piece in getPiecesWidthValidMoves(board, player1Color):
                for move in getValidMoves(board, piece):
                    newBoard = deepcopy(board)
                    newBoard = makeMove(newBoard, player2Color, piece, move)
                    value = self.minimax(newBoard, depth - 1, True, alpha, beta)
                    bestValue = min(bestValue, value)
                    beta = min(beta, bestValue)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return bestValue


    def getMove(self, board):
        bestPiece, bestMove = None, None
        bestScore = float("-inf")

        for piece in getPiecesWidthValidMoves(board, player2Color):
            for move in getValidMoves(board, piece):
                newBoard = deepcopy(board)
                newBoard = makeMove(newBoard, player2Color, piece, move)
                score = self.minimax(newBoard, 4, False, float("-inf"), float("inf"))
                print(score)
                if score > bestScore:
                    bestScore = score
                    bestPiece, bestMove = piece, move

        return bestPiece, bestMove
