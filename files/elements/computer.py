from ..misc.util import *
import random, pygame, sys, time
from copy import deepcopy
from multiprocessing import Manager
from tqdm import tqdm

class Computer:
    def __init__(self, playerColor) -> None:
        self.playerColor = playerColor
        self.depth = 7
        self.boardsAnalized = 0
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    def getPiecesInCenter(self, board, pieceColor):
        nPieces = 0
        for rowIndex,row in enumerate(board):
            for colIndex,col in enumerate(row):
                square = board[rowIndex][colIndex]

                if square != 0 and square.color == pieceColor:
                    if rowIndex > sqInHeight//3 and rowIndex < int(sqInHeight*0.66):
                        if colIndex > sqInWidth//3 and colIndex < int(sqInWidth*0.66):
                            nPieces += 1
        
        return nPieces
    
    def isInCenter(self, pieceCord):
        row, col = pieceCord
        if row > sqInHeight//3 and row < int(sqInHeight*0.66):
            if col > sqInWidth//3 and col < int(sqInWidth*0.66):
                return True
        return False

    def eval(self, board):
        player1Pieces = player2Pieces = player1Kings = player2Kings = 0
        player1SquareControl = player2SquareControl = 0
        player1PiecesInCenter = player2PiecesInCenter = 0

        for rowIndex,row in enumerate(board):
            for colIndex,col in enumerate(row):
                piece = board[rowIndex][colIndex]
                pieceCord = (rowIndex, colIndex)
                if piece != 0:
                    if piece.color == player1Color:
                        player1Pieces += 1

                        player1SquareControl += len(getValidMoves(board, pieceCord))

                        if piece.king:
                            player1Kings += 1

                        if self.isInCenter(pieceCord):
                            player1PiecesInCenter += 1

                    elif piece.color == player2Color:
                        player2Pieces += 1

                        player2SquareControl += len(getValidMoves(board, pieceCord))

                        if piece.king:
                            player2Kings += 1

                        if self.isInCenter(pieceCord):
                            player2PiecesInCenter += 1

        piecesScore = player2Pieces-player1Pieces
        kingsScore = player2Kings-player1Kings
        controlScore = player2SquareControl - player1SquareControl
        piecesInCenterScore = player2PiecesInCenter - player1PiecesInCenter

        return piecesScore + 2*kingsScore + controlScore + 2*piecesInCenterScore

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        self.events()
        if depth == 0 or checkWin(board):
            return self.eval(board)

        if maximizing_player:
            bestValue = float("-inf")
            for piece in getPiecesWidthValidMoves(board, player2Color):
                for move in getValidMoves(board, piece):
                    self.boardsAnalized += 1
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
                    self.boardsAnalized += 1
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
        
        for piece in tqdm(getPiecesWidthValidMoves(board, player2Color)):
            for move in getValidMoves(board, piece):
                newBoard = deepcopy(board)
                newBoard = makeMove(newBoard, player2Color, piece, move)
                score = self.minimax(newBoard, self.depth, False, float("-inf"), float("inf"))
                if score > bestScore:
                    bestScore = score
                    bestPiece, bestMove = piece, move
                    
        print("Boards analized:", str(self.boardsAnalized), "\n")
        self.boardsAnalized = 0

        return bestPiece, bestMove


