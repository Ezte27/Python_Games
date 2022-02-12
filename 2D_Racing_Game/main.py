import pygame, sys
from settings import *
from level import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock  = pygame.time.Clock()
        pygame.display.set_caption(TITLE)
        self.level1 = Level()
    
    def run(self):
        offset = pygame.math.Vector2()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        # Show map and menu
                        #self.level1.toggle_menu()
                        pass
            self.screen.fill('black')
            self.level1.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()