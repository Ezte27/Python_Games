import pygame
import random
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
RANDOM_COLORS = [[(202, 164, 114), (150, 75, 0)], [(140, 80, 0), (50, 50, 50)], [(255,233,197), (50, 50, 50)], [(250, 250, 250), (70, 70, 70)]]
colors = random.choice(RANDOM_COLORS)

def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 

# This will handle user input and update the graphics

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    sqSelected = ()
    playerClicks = []
    loadImages()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
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
                    if move in validMoves:
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # Reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()
    
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
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


if __name__ == "__main__":
    main()
