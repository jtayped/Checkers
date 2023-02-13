import pygame, sys
from files.settings import *
from .piece import Piece
from ..util import *

class Board:
    def __init__(self, screen, clock, mode, font) -> None:
        self.screen = screen
        self.clock = clock
        self.mode = mode
        self.font = font

        self.gameOver = False

        self.board = []
        self.initBoard()

        self.selectedPiece = None
        self.validMoves = None

        self.playerTurn = player1Color
        self.winner = None

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
                x, y = calculatePos(move[0][0], move[0][1])
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
    
    def checkWin(self):
        nPossibleMovesPlayer1 = nPossibleMovesPlayer2 = 0
        winner = None

        for row in range(sqInWidth):
            for col in range(sqInHeight):
                piece = self.board[row][col]
                if piece != 0:
                    if piece.color == player1Color:
                        nPossibleMovesPlayer1 += len(piece.getValidMoves(self.board))
                    if piece.color == player2Color:
                        nPossibleMovesPlayer2 += len(piece.getValidMoves(self.board))
        
        if nPossibleMovesPlayer1 == 0:
            winner = player2Color
        elif nPossibleMovesPlayer2 == 0:
            winner = player1Color
        
        return winner

    def makeMove(self, pieceCoord, move, kill, player):
        pieceRow, pieceCol = pieceCoord
        king = self.board[pieceRow][pieceCol].king
        self.board[pieceRow][pieceCol] = 0
    
        self.board[move[0]][move[1]] = Piece(self.screen, move[0], move[1], player, king)
        if type(kill) == list:
            self.board[kill[0]][kill[1]] = 0
        
        if (self.playerTurn == player1Color and move[0] == sqInHeight-1) or (self.playerTurn == player2Color and move[0] == 0):
            self.board[move[0]][move[1]].makeKing()

        if self.playerTurn == player1Color:
            self.playerTurn = player2Color
        else:
            self.playerTurn = player1Color

        self.validMoves = None
        self.winner = self.checkWin()

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
                if [row, col] == validMove[0]:
                    kill = validMove[1]
                    self.makeMove([self.selectedPiece.row, self.selectedPiece.col], [row, col], kill, self.playerTurn)
    
    def winnerManager(self):
        if self.winner == player1Color:
            winner = 'player1'
        else:
            winner = 'player2'

        if winner != None:
            text = self.font.render(f"Winner: {winner}", True, (50, 50, 50))
            textRect = text.get_rect()

            self.screen.blit(text, (WIDTH//2-textRect.width//2, HEIGHT//2-textRect.height//2))

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
        self.winnerManager()

        ###############################

        pygame.display.flip()
        self.clock.tick(FPS)
    
    def run(self):
        while not self.gameOver:
            self.update()