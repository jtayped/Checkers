from .settings import *
import pygame

def calculatePos(row, col):
    return (sqSize*col + sqSize//2, sqSize*row + sqSize//2)

def calculateCoord(x, y):
    return y//sqSize, x//sqSize

def drawSquares(screen):
    for row in range(sqInWidth):
        for col in range(row % 2, sqInWidth, 2):
            pygame.draw.rect(screen, BOARD_COLOR, (row*sqSize, col*sqSize, sqSize, sqSize))

def getPiecesWidthValidMoves(board, pieceColor):
    pieces = []
    for rowIndex,row in enumerate(board):
        for colIndex,col in enumerate(row):
            square = board[rowIndex][colIndex]
            if square != 0:
                if square.color == pieceColor and len(getValidMoves(board, (rowIndex, colIndex))) > 0:
                    pieces.append([rowIndex, colIndex])
    
    return pieces


def isValidMove(board, pieceCoord, moveCoord):
    # Get the current row and column of the piece
    row, col = pieceCoord
    piece = board[row][col]

    # Get the destination row and column
    destRow, destCol = moveCoord

    # Check if the square is occupied by the player's own piece
    if board[destRow][destCol] != 0 and board[destRow][destCol] != piece.color:
        return False
    
    # Check if the move is a valid jump over an opponent's piece
    if piece.color == player1Color:
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
        if jumpPos != 0 and ((destRow - row) * piece.direction > 0 or piece.king):
            if jumpPos.color == opponent and board[destRow][destCol] == 0:
                return True
    # Check if the move is a simple diagonal move
    if rowDiff == 1 and colDiff == 1:
        if (destRow - row) * piece.direction > 0 or piece.king:
            return True
    # If none of the above conditions are met, the move is not valid
    return False

def getValidMoves(board, pieceCord):
    row, col = pieceCord
    validMoves = []

    for indexRow,rowBoard in enumerate(board):
        for indexCol,colBoard in enumerate(rowBoard):
            if isValidMove(board, (row, col), (indexRow, indexCol)):
                validMoves.append([indexRow, indexCol])
    
    return validMoves

def checkWin(board):
    winner = None
    if len(getPiecesWidthValidMoves(board, player1Color)) == 0:
        winner = player2Color
    
    elif len(getPiecesWidthValidMoves(board, player2Color)) == 0:
        winner = player1Color
    
    return winner

def checkMoveMakesKing(row, playerColor):
    if playerColor == player1Color:
        if row == sqInHeight-1:
            return True
    elif playerColor == player2Color:
        if row == 0:
            return True
    return False