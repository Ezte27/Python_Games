"""
    Simple program to understand NEAT-python. In this program the ai will have ONE goal and it is to match the background color. THAT SIMPLE. The AI will have 3 input neurons with the rgb values of the background and it will have 3 output neurons which will return the rgb values for the color of the AI
"""
import math
import sys
from tabnanny import check
import pygame, neat, pickle
from random import randint, choice
from settings import *

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

    # Add Reporter
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    generation = 0
    winner = p.run(eval_genomes, MAX_GENERATIONS)
    # Save the winner
    with open('Python_Games/Simple_NEAT_AI/best_genome.pickle', 'wb') as f:
        pickle.dump(winner, f)