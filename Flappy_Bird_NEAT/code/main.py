import pygame
# Initializing Pygame First
pygame.init()
pygame.font.init()

import neat
import sys
from settings import *
from bird import Bird
from pipe import Pipe
from base import Base

class Game:
    def __init__(self, genomes, config) -> None:
        # NEAT Setup
        self.nets = []
        self.ge = []
        self.birds = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.birds.append(Bird(230, 350))
            g.fitness = 0
            self.ge.append(g)


        # Screen Setups
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        self.clock = pygame.time.Clock()

        # Pipes
        self.pipes = [Pipe(700)]

        # Base
        self.base = Base(630)

        # # Player
        # self.birds = [Bird((230, 350))]

    def run(self):
        self.screen.blit(BG_IMG, (0,0))

        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Drawing Score
        text = STAT_FONT.render("Score: " + str(self.bird.score), 1, (255,255,255))
        self.screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
        
        pipe_ind = 0
        if len(self.birds) > 0:
            if len(self.pipes) > 1 and self.birds[0].x > self.pipes[0].x + PIPE_WIDTH:
                pipe_ind = 1
        else:
            pygame.quit()
            sys.exit()

        for x, bird in enumerate(self.birds):
            bird.move()
            self.ge[x].fitness += 0.1

            output = self.nets[x].activate((bird.y, abs(bird.y - self.pipes[pipe_ind].height, abs(bird.y - self.pipes[pipe_ind].bottom))))

            if output[0] > 0.5:
                bird.jump()

        rem = []
        add_pipe = False
        for pipe in self.pipes:
            for x, bird in enumerate(self.birds):
                if pipe.collide(bird):
                    self.ge[x].fitness -= 1
                    self.birds.pop(x)
                    self.nets.pop(x)
                    self.ge.pop(x)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + PIPE_WIDTH < 0:
                rem.append(pipe)

            pipe.move()
        

        if add_pipe:
            for g in self.ge:
                g.fitness += 5
            self.pipes.append(Pipe(750))
        
        for r in rem:
            self.pipes.remove(r)
        
        for x, bird in enumerate(self.birds):
            if bird.y + bird.img.get_height() >= SCREEN_HEIGHT or bird.y < 0:
                self.birds.pop(x)
                self.nets.pop(x)
                self.ge.pop(x)

        self.base.move()
        self.base.draw(self.screen)

        # Player Update
        #self.bird.update_timers()
        # self.bird.input()
        # self.bird.move()
        for bird in self.birds:
            bird.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def neat_run(self, config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(x,50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    game = Game()
    game.neat_run(config_path)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        game.run()

pygame.quit()