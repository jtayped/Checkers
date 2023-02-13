import pygame, sys
from files.settings import *
from .piece import Piece
from ..util import *

class Board:
    def __init__(self, screen, clock, mode) -> None:
        self.screen = screen
        self.clock = clock
        self.mode = mode

        self.gameOver = False

        self.board = []
        self.initBoard()

        self.selectedPiece = None
        self.validMoves = None

        self.playerTurn = player1Color

    def initBoard(self):
        for row in range(sqInWidth):
            self.board.append([])
            for col in range(sqInHeight):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(self.screen, row, col, player1Color))
                    elif row > 4:
                        self.board[row].append(Piece(self.screen, row, col, player2Color))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    ##################################
    ########### DRAW BOARD ###########
    ##################################

    def drawValidMoves(self):
        if self.validMoves != None:
            for move in self.validMoves:
                x, y = calculatePos(move[0], move[1])
                pygame.draw.circle(self.screen, 'blue', (x,y), sqSize/10)

    def drawSquares(self):
        for row in range(sqInWidth):
            for col in range(row % 2, sqInWidth, 2):
                pygame.draw.rect(self.screen, BOARD_COLOR, (row*sqSize, col*sqSize, sqSize, sqSize))

    def drawPieces(self):
        for row in range(sqInWidth):
            for col in range(sqInHeight):
                piece = self.board[row][col]
                if piece != 0:
                    piece.update()

    def drawBoard(self):
        self.drawSquares()
        self.drawPieces()

    ##################################
    ##################################

    def makeMove(self, pieceCoord, move, player):
        pieceRow, pieceCol = pieceCoord
        self.board[pieceRow][pieceCol] = 0

        self.board[move[0]][move[1]] = Piece(self.screen, move[0], move[1], player)

        if self.playerTurn == player1Color:
            self.playerTurn = player2Color
        else:
            self.playerTurn = player1Color

        self.validMoves = None

    def getSquare(self):
        mx, my = pygame.mouse.get_pos()
        row, col = my//sqSize, mx//sqSize

        selectedSquare = self.board[row][col]
        if selectedSquare != 0:
            self.selectedPiece = selectedSquare
            if self.selectedPiece.color == self.playerTurn:
                self.validMoves = self.selectedPiece.getValidMoves(self.board)
        
        if selectedSquare == 0 and self.validMoves != None:
            for validMove in self.validMoves:
                if [row, col] == validMove:
                    self.makeMove([self.selectedPiece.row, self.selectedPiece.col], [row, col], self.playerTurn)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def update(self):
        self.events()
        self.screen.fill(BACKGROUND_COLOR)

        ######### Game Events #########
        
        if pygame.mouse.get_pressed()[0]:
            self.getSquare()

        self.drawBoard()
        self.drawValidMoves()

        ###############################

        pygame.display.flip()
        self.clock.tick(FPS)
    
    def run(self):
        while not self.gameOver:
            self.update()