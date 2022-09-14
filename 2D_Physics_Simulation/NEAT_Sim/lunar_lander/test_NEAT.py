import os
import pickle
from random import randint
import neat
import gym
import numpy as np
import matplotlib.pyplot as plt

local_dir = os.path.dirname(__file__)

with open(os.path.join(local_dir, 'stats/winner.pickle'), 'rb') as f:
    genome = pickle.load(f)

print('Loaded genome: ')
print(f"Fitness: {genome.fitness}")


config_path = os.path.join(local_dir, 'config.txt')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)

net = neat.nn.FeedForwardNetwork.create(genome, config)

env = gym.make("BipedalWalker-v3", render_mode="human")
observation, info = env.reset()

terminated = False
truncated = False

steps = 0
total_reward = 0
while True:
    action = net.activate(observation)

    observation, reward, terminated, truncated, info = env.step(action)
    
    steps += 1
    total_reward += reward

    if terminated or truncated or steps >= 400:
        break

print(f"step: {steps}, total_reward: {total_reward}")

env.close()