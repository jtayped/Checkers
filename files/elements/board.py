import pygame, sys
from files.settings import *
from .piece import Piece

class Board:
    def __init__(self, screen, clock, mode) -> None:
        self.screen = screen
        self.clock = clock
        self.mode = mode

        self.gameOver = False

        self.board = []
        self.initBoard()
        print(self.board)
        print(self.board[2][1].getPossibleMoves(self.board))
        self.selectedPiece = None

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
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def update(self):
        self.events()
        self.screen.fill(BACKGROUND_COLOR)

        ######### Game Events #########
        
        self.drawBoard()

        ###############################

        pygame.display.flip()
        self.clock.tick(FPS)
    
    def run(self):
        while not self.gameOver:
            self.update()