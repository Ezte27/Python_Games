import os, sys, warnings, time
from colorama import Fore
import pickle
from random import randint
import neat
import numpy as np
import matplotlib.pyplot as plt

import gym
import rocket_lander

FPS = 40
SLOW_MODE = True

local_dir = os.path.dirname(__file__)
genome_path = 'stats\winners\winner_16653831.pickle'
full_path = os.path.join(local_dir, genome_path)

try:
    with open(full_path, 'rb') as f:
        genome = pickle.load(f)

except FileNotFoundError:
    print(f"{Fore.RED}[ERROR] {Fore.RESET}File: \"{full_path}\" not found.")
    print(f"The genome is unavailable due to missing file ({genome_path})")
    time.sleep(1.5)

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

env = gym.make("RocketLander-v0", render_mode="human", clock=True, fps=FPS)

observation, info = env.reset()

done = False
truncated = False

steps = 0
reward_per_step = []

runs = 0
MAX_RUNS = 6

while runs < MAX_RUNS:
    try:
        action = np.argmax(net.activate(observation))
    except NameError:
        action = env.action_space.sample()
    
    if SLOW_MODE and (steps % 100 == 0):
        observation, reward, done, truncated, info = env.step(action)
    else:
        observation, reward, done, truncated, info = env.step(action)

    steps += 1
    reward_per_step.append(reward)

    if done or truncated:
        runs += 1
        observation, info = env.reset()

    # try:
    #     print(f"Observation: {Fore.BLUE}{observation}{Fore.RESET}, Reward: {Fore.GREEN if reward > 0 else Fore.RED}{reward}{Fore.RESET}")
    # except NameError:
    #     print(f"Observation: {observation}, Reward: {reward}")

    print(f"Action: {action}")
        
    if (done or truncated): print("FINISHED SIMULATION")

display_stats(steps, reward_per_step, filename = os.path.join(local_dir, 'stats/fitness.png'))

env.close()