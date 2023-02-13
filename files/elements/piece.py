import pygame
from ..settings import *
from ..util import *

class Piece:
    def __init__(self, screen, row, col, color, king=False) -> None:
        self.screen = screen
        self.row, self.col = row, col
        self.color = color
        self.king = king
        self.selected = False

        self.radius = sqSize*0.8//2
        self.crown = pygame.image.load('files/assets/crown.png')
        self.crown = pygame.transform.scale(self.crown, (self.radius, self.radius))

        if self.color == player1Color:
            self.direction = 1
        else:
            self.direction = -1

        self.x, self.y = calculatePos(row, col)
    
    def makeKing(self):
        self.king = True
    
    def select(self):
        self.selected = True
    
    def isValidMove(self, board, move):
        # Get the current row and column of the piece
        row, col = self.row, self.col
        # Get the destination row and column
        destRow, destCol = move
        # Check if the square is occupied by the player's own piece
        if board[destRow][destCol] != 0 and board[destRow][destCol] != self.color:
            return [False, False]
        # Check if the move is a valid jump over an opponent's piece
        if self.color == player1Color:
            opponent = player2Color
        else:
            opponent = player1Color
        # Check if the move is a diagonal move that involves jumping over an opponent's piece
        rowDiff = abs(row - destRow)
        colDiff = abs(col - destCol)
        if rowDiff == 2 and colDiff == 2:
            jumpRow = (row + destRow) // 2
            jumpCol = (col + destCol) // 2
            jumpPos = board[jumpRow][jumpCol]
            if jumpPos != 0 and ((destRow - row) * self.direction > 0 or self.king):
                if jumpPos.color == opponent and board[destRow][destCol] == 0:
                    return [True, [jumpRow, jumpCol]]
        # Check if the move is a simple diagonal move
        if rowDiff == 1 and colDiff == 1:
            if (destRow - row) * self.direction > 0 or self.king:
                return [True, False]
        # If none of the above conditions are met, the move is not valid
        return [False, False]

    def getValidMoves(self, board):
        possibleMoves = []
        for rowIndex,row in enumerate(board):
            for colIndex,col in enumerate(row):
                move = [rowIndex, colIndex]
                validMove = self.isValidMove(board, move)
                if validMove[0]:
                    possibleMoves.append([move, validMove[1]])
        return possibleMoves

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        if self.king:
            self.screen.blit(self.crown, (self.x-self.radius, self.y-self.radius))
    
    def update(self):
        self.draw()

    def __repr__(self) -> str:
        return self.color