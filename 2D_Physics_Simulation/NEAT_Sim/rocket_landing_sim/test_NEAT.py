import os, sys, warnings
import time
from colorama import Fore
import pickle
import neat
import gym
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

env = gym.make("RocketLander-v0", render_mode="human")
observation, info = env.reset()

terminated = False
truncated = False

runs = 0
MAX_RUNS = 10

steps = 0
total_reward = 0
reward_per_step = []
while runs < MAX_RUNS:
    try:
        action = np.argmax(net.activate(observation))
    except NameError:
        action = env.action_space.sample()
    #action = 0 if steps < 60 else 2

    # if action == 2 and steps > 80:
    #     time.sleep(1)

    observation, reward, terminated, truncated, info = env.step(action)
    
    steps += 1
    total_reward += reward
    reward_per_step.append(reward)
    print(observation)

    if terminated or truncated:
        runs += 1
        observation, info = env.reset()

print(f"step: {steps}, total_reward: {total_reward}")
display_stats(steps, reward_per_step, filename = os.path.join(local_dir, 'stats/fitness.png'))

env.close()