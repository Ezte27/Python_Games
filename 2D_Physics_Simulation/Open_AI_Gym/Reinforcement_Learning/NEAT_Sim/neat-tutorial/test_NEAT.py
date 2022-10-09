import os
import pickle
import neat
import gym
import numpy as np

local_dir = os.path.dirname(__file__)

with open(os.path.join(local_dir, 'winner.pickle'), 'rb') as f:
    genome = pickle.load(f)

print('Loaded genome: ')
print(genome)


config_path = os.path.join(local_dir, 'config.txt')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)

net = neat.nn.FeedForwardNetwork.create(genome, config)

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset()

terminated = False
truncated = False
while (not terminated) and (not truncated):
    action = np.argmax(net.activate(observation))

    observation, reward, terminated, truncated, info = env.step(action)
    env.render()
env.close()