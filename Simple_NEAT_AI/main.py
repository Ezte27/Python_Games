"""
    Simple program to understand NEAT-python. In this program the ai will have ONE goal and it is to match the background color. THAT SIMPLE. The AI will have 3 input neurons with the rgb values of the background and it will have 3 output neurons which will return the rgb values for the color of the AI
"""

import math
import sys
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
    bg_color = get_random_color()
    runs = 0
    
    if FAST_AI_TRAINING:
        while runs < FAST_COLOR_CHANGES_NUM:
            runs += 1

            bg_color = get_random_color()

            # Reset the colors of the players
            for player in players:
                player.reset_color()

            # Get AI Output
            for i, net in enumerate(nets):
                output = nets[i].activate(get_inputs(bg_color))
                #print(f"\n UNCHANGED: {output}") # DEBUG
                output = transform_output(output)
                #print(output)
                players[i].color = output

            # Update Fitness
            for i, genome in enumerate(ge):
                if check_color(players[i], bg_color):
                    genome.fitness += 10
                else:
                    genome.fitness -= 6
    
    else:
        start_time = 0

        running = True

        while running:

            clock.tick(FPS)

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
                    #print(f"\n UNCHANGED: {output}") # DEBUG
                    output = transform_output(output)
                    #print(output)
                    players[i].color = output

                # Update Fitness
                for i, genome in enumerate(ge):
                    if check_color(players[i], bg_color):
                        genome.fitness += 10
                    else:
                        genome.fitness -= 6
            
            # Drawing
            screen.fill(bg_color)

            for player in players:
                pygame.draw.rect(screen, player.color, player.rect)

            gen_text = font.render(f"Generation: {generation}", False, 'Black')
            gen_text_rect = gen_text.get_rect(topleft = (0, 0))
            screen.blit(gen_text, gen_text_rect)

            try:
                best_genome_fitness_text = font.render(f"Average fitness: {round(stats.get_fitness_mean()[generation - 2], 2)}", False, 'Black')
                best_genome_fitness_text_rect = best_genome_fitness_text.get_rect(topright = (SCREEN_WIDTH, 0))
                screen.blit(best_genome_fitness_text, best_genome_fitness_text_rect)
            
            except:
                pass
            
            pygame.display.update()

def test_ai(genome, config):

    # NEAT Setup
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    player = Player((SCREEN_WIDTH//2 - PLAYER_WIDTH, SCREEN_HEIGHT//2 - PLAYER_HEIGHT))

    bg_color = (255, 255, 255)
    accuracy = 0
    total = 0
    correct = 0

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

            # Keyboard Input
        # keys = pygame.key.get_pressed()
        # if True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    bg_color = get_random_color()
                    total += 1

                    # AI OUTPUT
                    output = net.activate(get_inputs(bg_color))
                    player.color = transform_output(output)

                    # Updating accuracy
                    if check_color(player, bg_color):
                        correct += 1  
                    else:
                        print(output) # DEBUG
                    accuracy = calculate_accuracy(correct, total)
                
                elif event.key == pygame.K_e:
                    for i in range(50000):
                        bg_color = get_random_color()
                        total += 1

                        # AI OUTPUT
                        output = net.activate(get_inputs(bg_color))
                        player.color = transform_output(output)

                        # Updating accuracy
                        if check_color(player, bg_color):
                            correct += 1  
                        accuracy = calculate_accuracy(correct, total)

        # Drawing
        pygame.draw.rect(screen, player.color, player.rect)

        gen_text = font.render(f"Accuracy: {round(accuracy, 2)}%", False, 'Black', 'White')
        gen_text_rect = gen_text.get_rect(topleft = (0, 0))
        screen.blit(gen_text, gen_text_rect)

        pygame.display.update()
        
def calculate_accuracy(correct, total):
    if total != 0:
        return (correct / total) * 100
    else:
        return 0

def check_color(player, bg_color):
    if player.color == bg_color:
        return True
    return False

def get_inputs(bg_color): # HAHAHA what a useless function!
    return bg_color

def transform_output(output):
    transformed_output = tuple(round(elem * 255) for elem in output)
    return transformed_output

def get_random_color():
    return choice(BG_COLORS)#tuple(randint(0, 255) for i in range(0, 3))#

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
    
    best_genome_path = f"{os.getcwd()}/best_genome.pickle"

    if input("Test or Train AI [0 / 1]") == '1':
        # Create core evolution class
        p = neat.Population(config)
        print(p.generation)

        # Add Reporter
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Run NEAT
        generation = 0

        winner = p.run(eval_genomes, MAX_GENERATIONS)

        # Save the winner
        with open(best_genome_path, 'wb') as f:
            pickle.dump(winner, f)
    
    else:
        with open(best_genome_path, 'rb') as f:
            genome = pickle.load(f)
        test_ai(genome, config)