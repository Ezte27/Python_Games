# OLD VERSION

"""
    Simple program to understand NEAT-python. In this program the AI tries to catch its prey. The AI's input = (AI_position, prey_position), The AI's output = (x_vel, y_vel)
"""
import math
import sys
from tabnanny import check
import pygame, neat, pickle
from random import randint, choice
from settings import *

class Game:
    def __init__(self, networks, players) -> None:
        self.networks = networks
        self.players = players
        
        self.create_prey()
        self.obstacles = self.create_obstacles()

    def train_ai(self, genomes, config, dt):
        global running
        # Output of the network
        for index, player in enumerate(self.players):
            output = self.networks[index].activate(self.get_inputs(player))
            player.x_vel += output[0] # The x_vel
            player.y_vel -= output[1] # The y_vel
            
            # Fitness
            
            distance = self.get_distance(player)
            if distance < player.last_distance:
                genomes[index][1].fitness += 3
            else:
                if not(self.check_collision(index)):
                    genomes[index][1].fitness -= 0.5
            
            # Update the player
            player.update(dt, distance)
        
        # Fitness update
        self.check_prey_player_collision(genomes)

    def get_inputs(self, player):
        return (player.rect.centerx - self.prey.rect.centerx, player.rect.centery - self.prey.rect.centery)

    def get_distance(self, player):
        return math.sqrt((player.rect.centerx - self.prey.rect.centerx)**2 + (player.rect.centery - self.prey.rect.centery)**2)

    def create_prey(self):
        self.prey = Prey()

    def move_prey(self): # Maybe??
        pass

    def check_prey_player_collision(self, genomes):
        for index, player in enumerate(self.players):
            if player.rect.colliderect(self.prey.rect):
                genomes[index][1].fitness += 10
            # else:
            #     genomes[index][1].fitness -= 0.0005 # No Prey = BAD
    
    def check_collision(self, index):
        if self.players[index].rect.colliderect(self.prey.rect):
            return True
        return False

    def create_obstacles(self): # Maybe??
        pass

class Prey:
    def __init__(self, pos = None, color = None) -> None:
        self.rect = pygame.Rect(pos[0], pos[1], PREY_WIDTH, PREY_HEIGHT) if pos else pygame.Rect(randint(0, SCREEN_WIDTH - PREY_WIDTH), randint(0, SCREEN_HEIGHT - PREY_HEIGHT), PREY_WIDTH, PREY_HEIGHT)
        self.color = color if color else choice(PREY_COLORS)


class Player:
    def __init__(self, pos = None, color = None) -> None:

        # General Setup
        self.rect = pygame.Rect((randint(0, SCREEN_WIDTH - PLAYER_WIDTH), randint(0, SCREEN_HEIGHT - PLAYER_HEIGHT)), (PLAYER_WIDTH, PLAYER_HEIGHT)) if not(pos) else pygame.Rect((pos), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.color = color if color else PLAYER_COLOR

        # Movement
        self.x_vel = 0
        self.y_vel = 0

        self.last_distance = 0
    
    def update(self, dt, distance):
        self.last_distance = distance

        self.rect.centerx += self.x_vel * dt
        self.rect.centery += self.y_vel * dt

def eval_genome(genomes, config):
    global generation, running
    generation += 1

    networks = []
    players  = []
    
    for i, (genome_id, genome) in enumerate(genomes):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)

        genome.fitness = 0

        players.append(Player())

    screen = pygame.display.get_surface()
    start_time = pygame.time.get_ticks()

    # Main Loop
    game = Game(networks, players)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        time_left = pygame.time.get_ticks() - start_time
        # game.prey.rect.center = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check time
        if time_left >= GENERATION_TIME:
            break

        game.train_ai(genomes, config, dt)

        # Drawing
        screen.fill('White')

        # Draw players
        for player in game.players:
            pygame.draw.rect(screen, player.color, player.rect)
        
        # Draw prey
        pygame.draw.rect(screen, game.prey.color, game.prey.rect)

        # Draw font
        gen_text = font.render("Generation: " + str(generation), False, 'Black')
        gen_text_rect = gen_text.get_rect(topleft = (10, 10))
        screen.blit(gen_text, gen_text_rect)

        time_left_text = font.render("Time: " + str(round(time_left/1000, 1)), False, 'Black')
        time_left_text_rect = time_left_text.get_rect(topleft = (10, gen_text_rect.height + 10))
        screen.blit(time_left_text, time_left_text_rect)

        pygame.display.update()

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
    winner = p.run(eval_genome, MAX_GENERATIONS)
    # Save the winner
    with open('Python_Games/Simple_NEAT_AI/best_genome.pickle', 'wb') as f:
        pickle.dump(winner, f)