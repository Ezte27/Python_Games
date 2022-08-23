import pygame
# Initializing Pygame First
pygame.init()
pygame.font.init()

import neat
from settings import *
from bird import Bird
from pipe import Pipe
from base import Base

class Game:
    def __init__(self) -> None:
        
        # Screen Setups
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        self.clock = pygame.time.Clock()

        # Pipes
        self.pipes = [Pipe(700)]

        # Base
        self.base = Base(630)

        # Player
        self.bird = Bird((230, 350))

    def run(self):
        self.screen.blit(BG_IMG, (0,0))

        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Drawing Score
        text = STAT_FONT.render("Score: " + str(self.bird.score), 1, (255,255,255))
        self.screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
        
        rem = []
        add_pipe = False
        for pipe in self.pipes:
            if pipe.collide(self.bird):
                pass
            
            if pipe.x + PIPE_WIDTH < 0:
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < self.bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()
        

        if add_pipe:
            self.bird.score += 1
            self.pipes.append(Pipe(750))
        
        for r in rem:
            self.pipes.remove(r)
        
        if self.bird.y + self.bird.img.get_height() >= SCREEN_HEIGHT:
            pass

        self.base.move()
        self.base.draw(self.screen)

        # Player Update
        #self.bird.update_timers()
        self.bird.input()
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