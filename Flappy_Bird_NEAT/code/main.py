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
    def __init__(self, config_path) -> None:
        # Screen Setups
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        self.clock = pygame.time.Clock()

        self.gen = 0

        # NEAT Setup
        self.neat_run(config_path)
        
    def eval_genomes(self, genomes, config):
        self.gen += 1
        self.nets = []
        self.ge = []
        self.birds = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.birds.append(Bird((230, 350)))
            g.fitness = 0
            self.ge.append(g)
        
        # Pipes
        self.pipes = [Pipe(700)]

        # Base
        self.base = Base(630)

        # # Player
        # self.birds = [Bird((230, 350))]
        self.score = 0
        self.run()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.screen.blit(BG_IMG, (0,0))

            for pipe in self.pipes:
                pipe.draw(self.screen)

            # Drawing Score
            text_score = STAT_FONT.render("Score: " + str(self.score), 1, (255,255,255))
            self.screen.blit(text_score, (SCREEN_WIDTH - 10 - text_score.get_width(), 10))

            # Drawing Generation
            text_gen = STAT_FONT.render("Gen: " + str(self.gen), 1, (255,255,255))
            self.screen.blit(text_gen, (SCREEN_WIDTH - 30 - text_gen.get_width() - text_score.get_width(), 10))
            
            pipe_ind = 0
            if len(self.birds) > 0:
                if len(self.pipes) > 1 and self.birds[0].x > self.pipes[0].x + PIPE_WIDTH:
                    pipe_ind = 1
            else:
                running = False

            for x, bird in enumerate(self.birds):
                bird.move()
                self.ge[x].fitness += 0.06

                output = self.nets[x].activate((bird.y, abs(bird.y - self.pipes[pipe_ind].height), abs(bird.y - self.pipes[pipe_ind].bottom)))

                if output[0] > 0.5:
                    bird.jump()

            rem = []
            add_pipe = False
            for pipe in self.pipes:
                pipe.move()
                for x, bird in enumerate(self.birds):
                    if pipe.collide(bird):
                        self.ge[x].fitness -= 2
                        self.birds.pop(x)
                        self.nets.pop(x)
                        self.ge.pop(x)
                    
                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True
                
                if pipe.x + PIPE_WIDTH < 0:
                    rem.append(pipe)
            

            if add_pipe:
                self.score += 1
                for g in self.ge:
                    g.fitness += 5
                self.pipes.append(Pipe(SCREEN_WIDTH*1.4))
            
            for r in rem:
                self.pipes.remove(r)
            
            for x, bird in enumerate(self.birds):
                if bird.y + bird.img.get_height() >= SCREEN_HEIGHT - (SCREEN_HEIGHT - self.base.y) or bird.y < 0:
                    self.ge[x].fitness -= 2
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
            
            if self.score >= 20:
                running = False

            pygame.display.update()

    def neat_run(self, config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.eval_genomes,50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    game = Game(config_path)

    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #             pygame.quit()

    #     game.run()
    print(game.gen)
pygame.quit()