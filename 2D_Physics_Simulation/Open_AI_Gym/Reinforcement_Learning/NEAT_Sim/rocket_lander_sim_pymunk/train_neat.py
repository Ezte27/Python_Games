"""
Booster lander experiment using a feed-forward neural network.
"""

import multiprocessing
import os
import pickle

import neat
import numpy as np

from visualize import plot_stats, plot_species

import gym
import rocket_lander

CHECKPOINT_INTERVAL = 15
MAX_GENERATIONS     = 20

runs_per_net = 2

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for _ in range(runs_per_net):
        env = gym.make("RocketLander-v0")

        observation, info = env.reset()

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        done = False
        truncated = False
        while all([(not done), (not truncated)]):
    
            output = net.activate(observation)
            action = np.argmax(output)

            observation, reward, done, truncated, info = env.step(action)

            fitness += reward

        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    return np.mean(fitnesses)

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    #pop = neat.Checkpointer.restore_checkpoint(os.path.join(local_dir, 'neat-checkpoint-797'))
    
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.Checkpointer(CHECKPOINT_INTERVAL))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate, MAX_GENERATIONS)

    # Save the winner.
    with open(os.path.join(local_dir, 'stats/winner.pickle'), 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    # Display the results
    plot_stats(stats, ylog=False, view=True, filename=os.path.join(local_dir, "stats/feedforward-fitness.png"))
    plot_species(stats, view=True, filename=os.path.join(local_dir, "stats/feedforward-speciation.png"))

if __name__ == '__main__':
    run()