import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        self.clock = pygame.time.Clock()

        self.level = Level()

        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                
                if event.type == pygame.KEYDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_LCTRL] and keys_pressed[pygame.K_c]:
                        self.running = False
            
            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()

    pygame.quit()