import pygame, sys
from ..misc.settings import *
from ..misc.util import *
from ..elements.piece import Piece
from ..elements.computer import Computer

class Board:
    def __init__(self, screen, clock, mode, winnerFont, subtitleFont) -> None:
        self.screen = screen
        self.clock = clock
        self.mode = mode
        self.winnerFont = winnerFont
        self.subtitleFont = subtitleFont

        self.gameOver = False
        self.turn = player1Color
        self.selectedPiece = None
        self.winner = None

        self.board = self.initBoard()

        self.computer = Computer(player2Color)

    def initBoard(self):
        board = []
        # Loop through each row in the board
        for row in range(sqInWidth):
            # Add a new row to the board
            board.append([])
            # Loop through each column in the current row
            for col in range(sqInHeight):
                # Check if the current position should contain a piece
                if col % 2 == ((row + 1) % 2):
                    # If the current row is less than 3, add a piece for player 1
                    if row < 3:
                        board[row].append(Piece(self.screen, row, col, player1Color))
                    # If the current row is greater than 4, add a piece for player 2
                    elif row > 4:
                        board[row].append(Piece(self.screen, row, col, player2Color))
                    # If the current row is between 3 and 4, add 0 to the board
                    else:
                        board[row].append(0)
                # If the current position should not contain a piece, add 0 to the board
                else:
                    board[row].append(0)
        return board

    def drawValidMoves(self, selectedPiece):
        validMoves = getValidMoves(self.board, selectedPiece)
        for move in validMoves:
            rowMove, colMove = move
            x, y = calculatePos(rowMove, colMove)
            pygame.draw.circle(self.screen, 'blue', (x, y), 10)

    def selectPiece(self, pieceCord):
        row, col = pieceCord
        self.selectedPiece = (row, col)

    def pieceSelectManager(self):
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            row, col = calculateCoord(mx, my)
            self.selectedSquare = self.board[row][col]

            if self.selectedSquare != 0:
                if self.selectedSquare.color == self.turn:
                    self.selectPiece((row, col))

    def drawPieces(self):
        for row in range(sqInWidth):
            for col in range(sqInHeight):
                piece = self.board[row][col]
                if piece != 0:
                    piece.update()

    def drawBoard(self):
        drawSquares(self.screen)
        self.drawPieces()

    def invertTurn(self, turn):
        if turn == player1Color:
            return player2Color
        else:
            return player1Color 

    def makeMove(self, board, piece, move):
        pieceRow, pieceCol = piece
        moveRow, moveCol = move
        
        board[pieceRow][pieceCol].move(moveRow, moveCol)

        board[moveRow][moveCol] = board[pieceRow][pieceCol]
        board[pieceRow][pieceCol] = 0

        if checkMoveMakesKing(moveRow, self.turn):
            board[moveRow][moveCol].makeKing()

        rowDiff, colDiff = abs(pieceRow - moveRow), abs(pieceCol - moveCol)

        if rowDiff == 2 and colDiff == 2:

            jumpRow, jumpCol = (pieceRow + moveRow) // 2, (pieceCol + moveCol) // 2
            jumpPos = board[jumpRow][jumpCol]
            if jumpPos.color == self.invertTurn(self.turn):
                board[jumpRow][jumpCol] = 0

        self.selectedPiece = None

        self.turn = self.invertTurn(self.turn)
        
        self.winner = checkWin(self.board)

        if self.mode == 'pvc' and self.turn == player2Color and self.winner == None:
            computerMove = self.computer.getMove(board)
            self.makeMove(self.board, computerMove[0], computerMove[1])

        return board

    def moveManger(self):
        if pygame.mouse.get_pressed()[0] and self.selectedPiece != None:
            mx, my = pygame.mouse.get_pos()
            row, col = calculateCoord(mx, my)
            if isValidMove(self.board, (self.selectedPiece), (row, col)):
                self.board = self.makeMove(self.board, self.selectedPiece, (row, col))

    def winnerMessage(self):
        winner = None
        if self.winner == player1Color:
            winner = 'player 1'
        elif self.winner == player2Color:
            winner = 'player 2'
        
        winnerMessage = self.winnerFont.render(f'Winner: {winner}', True, (50, 50, 50))
        winnerRect = winnerMessage.get_rect()

        x, y = WIDTH//2-winnerRect.width//2, HEIGHT//2-winnerRect.height//2
        self.screen.blit(winnerMessage, (x, y))

        instruction = self.subtitleFont.render("Press M to go to the menu!", True, (50, 50, 50))
        instructionRect = instruction.get_rect()

        self.screen.blit(instruction, (WIDTH//2-instructionRect.width//2, y+winnerRect.height//1.5))

        key = pygame.key.get_pressed()
        if key[pygame.K_m]:
            self.gameOver = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()



    def update(self):
        self.events()
        self.screen.fill(BACKGROUND_COLOR)

        ######### Game Events #########

        self.pieceSelectManager()
        self.drawBoard()

        if self.selectedPiece != None:
            self.drawValidMoves(self.selectedPiece)

        self.moveManger()

        if self.winner != None:
            self.winnerMessage()

        ###############################

        pygame.display.flip()
        self.clock.tick(FPS)


    def run(self):
        self.__init__(self.screen, self.clock, self.mode, self.winnerFont, self.subtitleFont)
        while not self.gameOver:
            self.update()