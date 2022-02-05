import pygame, sys

pygame.init()
screen = pygame.display.set_mode((100, 100))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()