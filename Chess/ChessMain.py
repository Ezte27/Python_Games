import pygame
import random
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
RANDOM_COLORS = [[(250, 250, 250), (70, 70, 70)]] #[[(202, 164, 114), (150, 75, 0)], [(140, 80, 0), (50, 50, 50)], [(255,233,197), (50, 50, 50)], [(250, 250, 250), (70, 70, 70)]]
colors = random.choice(RANDOM_COLORS)

def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(r"C:\Users\ested\Documents\Programming\Python_Games\Chess\images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 

# This will handle user input and update the graphics

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    sqSelected = ()
    playerClicks = []
    loadImages()
    running = True
    gameOver = False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = pygame.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                print(move.getChessNotation())
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # Reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == pygame.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                if e.key == pygame.K_q:
                    running = False

        if moveMade:
            if animate:
                animatingMoves(screen, gs.moveLog[-1], gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, sqSelected)
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate!")
            else:
                drawText(screen, "White wins by checkmate!")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate!")
        clock.tick(MAX_FPS)
        pygame.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value. 0 = transparent, 255 = opaque
            s.fill(pygame.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(c+r)%2]
            pygame.draw.rect(screen, pygame.Color(color), pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE, SQ_SIZE))

def animatingMoves(screen, move, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = pygame.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], (c*SQ_SIZE, r*SQ_SIZE))
        pygame.display.flip()
        clock.tick(30)
def drawText(screen, text):
    font = pygame.font.SysFont("Helvitca", 40, True, False)
    textObject = font.render(text, 0, pygame.Color("Black"))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color("gray"))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main__":
    main()
