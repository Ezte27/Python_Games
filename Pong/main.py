from settings import *
from game import Game
import pygame
import neat
import os
import pickle

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_NAME)



class PongGame:
    def __init__(self, window, ai=False):
        self.game = Game(window, ai=ai)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball
    
    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            if not self.game.running: # Check if player won
                run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=False, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=False, up=False)

            output = net.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision = output.index(max(output))
            print(decision)
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=True, up=True)
            elif decision == 2:
                self.game.move_paddle(left=True, up=False)
            
            self.game.loop()
            
        pygame.quit()
    
    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        #net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            #output2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision1 = output1.index(max(output1))
            #decision2 = output2.index(max(output2))

            if decision1 == 0:
                genome1.fitness -= 0.01
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            elif decision1 == 2:
                self.game.move_paddle(left=True, up=False)
            
            self.game.ai_monster(left=False)
            # if decision2 == 0:
            #     #genome1.fitness -= 0.01
            #     pass
            # elif decision2 == 1:
            #     self.game.move_paddle(left=False, up=True)
            # elif decision2 == 2:
            #     self.game.move_paddle(left=False, up=False)

            self.game.loop()

            if not self.game.running or self.game.left_player_hits > 30: # Check if player won or too many hits
                self.calculate_fitness(genome1, genome2)
                break
    
    def calculate_fitness(self, genome1, genome2):
        genome1.fitness += self.game.left_player_hits
        #genome2.fitness += self.game.right_player_hits
        genome1.fitness -= self.game.left_player_misses * 0.1
        #genome2.fitness -= self.game.right_player_misses * 0.1

def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        # if i == len(genomes) - 1:
        #     break
        genome1.fitness = 0
        game = PongGame(window, ai=True)
        game.train_ai(genome1, 'genome2', config)
        # for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
        #     genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
        #     game = PongGame(window, ai=False)
        #     game.train_ai(genome1, genome2, config)

def run_neat(config):
    #population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-19')
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(2))

    winner = population.run(eval_genomes, 80)
    with open('Python_Games/Pong/best_genome.pickle', 'wb') as f:
        pickle.dump(winner, f)

def test_ai(config):
    with open('Python_Games/Pong/best_genome.pickle', 'rb') as f:
        genome = pickle.load(f)
    game = PongGame(window)
    game.test_ai(genome, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    run_neat(config) if input("run or test the ai [r/t]") == 'r' else test_ai(config)