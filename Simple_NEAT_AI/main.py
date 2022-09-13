"""
    Simple program to understand NEAT-python. In this program the ai will have ONE goal and it is to match the background color. THAT SIMPLE. The AI will have 3 input neurons with the rgb values of the background and it will have 3 output neurons which will return the rgb values for the color of the AI
"""

import math
import sys
from tabnanny import check
import pygame, neat, pickle
from random import randint, choice
from settings import *

class Player:
    def __init__(self, pos, color = 'White') -> None:
        self.rect = pygame.Rect((pos), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.color = color
        self.original_color = color
    
    def reset_color(self):
        self.color = self.original_color

def eval_genomes(genomes, config):
    global generation
    generation += 1
    nets = []
    ge = []
    players = []

    for _, (_, genome) in enumerate(genomes):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player((randint(0, SCREEN_WIDTH - PLAYER_WIDTH), randint(0, SCREEN_HEIGHT - PLAYER_HEIGHT))))

        genome.fitness = 0
        ge.append(genome)
    
    run(nets, ge, players)

def run(nets, ge, players):
    bg_color = choice(BG_COLORS)
    print(f"\n BACKGROUND COLOR: {bg_color}\n")
    
    start_time = 0
    runs = 0

    running = True
    while running:

        clock.tick(FPS)
        screen.fill(bg_color)

        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        if pygame.time.get_ticks() - start_time >= COLOR_DURATION: # Checks for new round
            start_time = pygame.time.get_ticks()
            if runs >= COLOR_CHANGES_NUM:
                running = False

            runs += 1

            bg_color = get_random_color()

            # Reset the colors of the players
            for player in players:
                player.reset_color()

            # Get AI Output
            for i, net in enumerate(nets):
                output = nets[i].activate(get_inputs(bg_color))
                # print(output) # DEBUG
                output = transform_output(output)
                players[i].color = output

            # Update Fitness
            for i, genome in enumerate(ge):
                if check_color(players[i], bg_color):
                    genome.fitness += 10
                else:
                    genome.fitness -= 6
        
        # Drawing
        for player in players:
            pygame.draw.rect(screen, player.color, player.rect)

        gen_text = font.render(f"Generation: {generation}", False, 'Black')
        gen_text_rect = gen_text.get_rect(topleft = (0, 0))
        screen.blit(gen_text, gen_text_rect)
        try:
            best_genome_fitness_text = font.render(f"Best fitness: {stats.best_genome().fitness}", False, 'Black')
            best_genome_fitness_text_rect = best_genome_fitness_text.get_rect(topright = (SCREEN_WIDTH, 0))
            screen.blit(best_genome_fitness_text, best_genome_fitness_text_rect)
        except:
            pass

        pygame.display.update()

def check_color(player, bg_color):
    if player.color == bg_color:
        return True
    return False

def get_inputs(bg_color): # HAHAHA what a useless function!
    return bg_color

def transform_output(output):
    transformed_output = tuple(round(elem * 255, 0) for elem in output)
    return transformed_output

def get_random_color():
    return tuple(randint(0, 255) for i in range(0, 3))#choice(BG_COLORS)

if __name__ == '__main__':
    # Pygame Setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_CAPTION)
    font = pygame.font.SysFont("Arial", 30)
    clock = pygame.time.Clock()

    # NEAT-python configuration

    config_path = CONFIG_PATH
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    # Create core evolution class
    p = neat.Population(config)
    print(p.generation)

    # Add Reporter
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    generation = 0

    winner = p.run(eval_genomes, 5)#MAX_GENERATIONS)
    # Save the winner
    best_genome_path = f"{os.getcwd()}/best_genome.pickle"
    with open(best_genome_path, 'wb') as f:
        pickle.dump(winner, f)