import os, sys, warnings
from colorama import Fore
import pickle
from random import randint
import neat
import gym
import numpy as np
import matplotlib.pyplot as plt

local_dir = os.path.dirname(__file__)
genome_path = 'stats/winner.pickle'
full_path = os.path.join(local_dir, genome_path)

try:
    with open(full_path, 'rb') as f:
        genome = pickle.load(f)

except FileNotFoundError:
    print(f"{Fore.RED}[ERROR] {Fore.RESET}File: \"{full_path}\" not found.")
    print(f"The genome is unavailable due to missing file ({genome_path})")

if 'genome' in locals():
    print('Loaded genome: ')
    print(f"Fitness: {genome.fitness}")

    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()

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

terminated = False
truncated = False

steps = 0
total_reward = 0
reward_per_step = []
while True:
    try:
        action = np.argmax(net.activate(observation))
    except NameError:
        action = env.action_space.sample()

    observation, reward, terminated, truncated, info = env.step(action)
    
    steps += 1
    total_reward += reward
    reward_per_step.append(reward)

    if terminated or truncated or steps >= 400:
        break

print(f"step: {steps}, total_reward: {total_reward}")
display_stats(steps, reward_per_step, filename = os.path.join(local_dir, 'stats/fitness.svg'))

env.close()