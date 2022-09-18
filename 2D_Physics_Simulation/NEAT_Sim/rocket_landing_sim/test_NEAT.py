import os, sys, warnings
import time
from colorama import Fore
import pickle
import neat
import gym
import pygame
import numpy as np
import matplotlib.pyplot as plt
import rocket_lander_gym

local_dir = os.path.dirname(__file__)
genome_path = 'stats/winner.pickle'
full_path = os.path.join(local_dir, genome_path)

try:
    with open(full_path, 'rb') as f:
        genome = pickle.load(f)

except FileNotFoundError:
    print(f"{Fore.RED}[ERROR] {Fore.RESET}File: \"{full_path}\" not found.")
    print(f"The genome is unavailable due to missing file ({genome_path})")

except EOFError:
    print(f"{Fore.RED}[ERROR]{Fore.RESET} Read beyond end of file")
    print(f"The genome is unavailable due to empty file ({genome_path})")

if 'genome' in locals():
    print('Loaded genome: ')
    print(f"Fitness: {genome.fitness}")

    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

def display_stats(steps:int, fitness_per_step: list, view:bool = True, ylog:bool = False, filename:str ='stats/fitness.svg'):
    if plt is None:
        warnings.warn("This display is unavailable due to missing dependency (matplotlib)")
    frames = range(steps)
    fitness = np.array(fitness_per_step)

    plt.plot(frames, fitness, 'b-', label="best")

    plt.title("Genome's fitness during test")
    plt.xlabel("Steps")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")
    if ylog:
        plt.gca().set_yscale('symlog')

    try:
        plt.savefig(filename)
    except FileNotFoundError:
        print(f"plt.savefig(filename) unavailable because {Fore.RED}FileNotFoundError{Fore.RESET}")

    if view:
        plt.show()

    plt.close()

def render_font(font, text, display):
    text_surf = font.render(text, False, 'Black')
    text_rect = text_surf.get_rect(topleft = (10, 10))
    display.blit(text_surf, text_rect)
    pygame.display.update()

env = gym.make("RocketLander-v0", render_mode="human")
observation, info = env.reset()

display_surface = pygame.display.get_surface()
font = pygame.font.SysFont('ariel', 20)

terminated = False
truncated = False

MANUAL_CONTROL = True

runs = 0
MAX_RUNS = 4

steps                 = 0
total_steps           = 0
total_reward          = 0
reward_per_step       = []
total_reward_per_step = []
while runs < MAX_RUNS:
    steps += 1
    total_steps += 1
    if MANUAL_CONTROL:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            action = 2

        elif keys[pygame.K_s]:
            action = 3
        
        elif keys[pygame.K_a]:
            action = 4

        elif keys[pygame.K_d]:
            action = 5
        
        elif keys[pygame.K_LEFT]:
            action = 0
        
        elif keys[pygame.K_RIGHT]:
            action = 1
        
        else:
            action = 6
    
    else:
        try:
            action = np.argmax(net.activate(observation))

        except NameError:
            action = env.action_space.sample()
            print('OHO')

    #action = 6 if action == 2 and steps < 190 else action

    # if 250 < steps < 300:
    #     time.sleep(1)

    observation, reward, terminated, truncated, info = env.step(action)
    
    print(reward)

    total_reward += reward
    reward_per_step.append(reward)
    total_reward_per_step.append(total_reward)
    
    render_font(font, str(steps), display_surface)

    if terminated or truncated:
        runs += 1
        steps = 0
        observation, info = env.reset()

print(f"total_steps: {total_steps}, total_reward: {total_reward}")
display_stats(total_steps, reward_per_step, filename = os.path.join(local_dir, 'stats/fitness1.png'))
display_stats(total_steps, total_reward_per_step, filename = os.path.join(local_dir, 'stats/fitness2.png'))

env.close()