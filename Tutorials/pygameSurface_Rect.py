import pygame, sys

# VARIABLES
WHITE = (255, 255, 255)
GREEN = (50, 250, 35)
BLUE = (25, 60, 250)

WIDTH = 500
HEIGHT = 500
FPS = 60
PLAYER_SPEED = 1
x_pos = 0
y_pos = 250
w = 100
h = 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


clock = pygame.time.Clock()
test_surface = pygame.Surface((w, h))
test_surface.fill(BLUE)
test_rect = test_surface.get_rect(center = (250, 250))

run = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(GREEN)
    if test_rect.left != WIDTH:
        test_rect.right += PLAYER_SPEED
    else:
        test_rect.right = 0
    screen.blit(test_surface, test_rect)
    pygame.display.update()
    clock.tick(FPS)