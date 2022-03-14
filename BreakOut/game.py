import pygame
from main import Main

class Game:
    def __init__(self):
        self.game = Main()
        self.play_ai = False
        self.main_menu()
    
    def main_menu(self): # Start menu ask if want to play or watch ai play or change game settings or see game controls
        self.play()
    
    def play(self):

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            if not self.game.running: # Check if player won
                #self.main_menu()
                pass

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.game.move_paddle(right = False)
            elif keys[pygame.K_d]:
                self.game.move_paddle(right = True)
            elif keys[pygame.K_r]:
                self.game.reset
            elif keys[pygame.K_q]: # Back to main menu
                pass
            elif keys[pygame.K_m]: # Show player or ai stats
                pass
            
            self.game.game_loop()
            
        pygame.quit()

    def the_ai_plays(self):
        pass

    def show_settings(self):
        pass

    def train_ai(self):
        pass

if __name__ == '__main__':
    Game()