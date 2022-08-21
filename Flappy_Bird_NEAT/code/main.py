import pygame
import neat
import random
from settings import *
from bird import Bird

class Game:
    def __init__(self) -> None:
        
        # Screen Setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        self.clock = pygame.time.Clock()

        # Player
        self.bird = Bird((250, 80))

    def run(self):
        self.screen.blit(BG_IMG, (0,0))
        self.bird.move()
        self.bird.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

if __name__ == '__main__':
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.run()

pygame.quit()