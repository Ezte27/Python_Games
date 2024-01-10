# To activate conda env:
# C:\Users\ested\anaconda3\Scripts\activate.bat
from level import *
from config import *
from debug import debug # Used for debugging purposes and initializes pygame for the entire game
import sys
import pygame

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock  = pygame.time.Clock()
        pygame.display.set_caption(TITLE)
        self.level1 = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()   
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_LCTRL] and keys_pressed[pygame.K_c]:
                        # Exit game
                        pygame.quit()   
                        sys.exit()
                    if keys_pressed[pygame.K_m]:
                        # Show map and menu
                        self.level1.toggle_menu()

            self.screen.fill('black')
            self.level1.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()