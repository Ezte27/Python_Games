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

input_for_control = input('MANUAL_CONTROL = ')
MANUAL_CONTROL = True if input_for_control == 'True' or input_for_control == '1' else False

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

def heuristic(env, s):
    """
    The heuristic for
    1. Testing
    2. Demonstration rollout.

    Args:
        env: The environment
        s (list): The state. Attributes:

            s[0] is the horizontal coordinate
            s[1] is the vertical coordinate
            s[7] is the horizontal speed
            s[8] is the vertical speed
            s[2] is the angle
            s[9] is the angular speed
            s[3] 1 if first leg has contact, else 0
            s[4] 1 if second leg has contact, else 0

    Returns:
         a: The heuristic to be fed into the step function defined above to determine the next step and reward.
    """

    # Changes for passing observation through heuristics
    s[1] += 1

    angle_targ = s[0] * 0.5 + s[7] * 1.0  # angle should point towards center
    if angle_targ > 0.4:
        angle_targ = 0.4  # more than 0.4 radians (22 degrees) is bad
    if angle_targ < -0.4:
        angle_targ = -0.4
    hover_targ = 0.55 * np.abs(
        s[0]
    )  # target y should be proportional to horizontal offset

    angle_todo = (angle_targ - s[2]) * 0.5 - (s[9]) * 1.0
    hover_todo = (hover_targ - s[1]) * 0.5 - (s[8]) * 0.5

    if s[3] or s[4]:  # legs have contact
        angle_todo = 0
        hover_todo = (
            -(s[8]) * 0.5
        )  # override to reduce fall speed, that's all we need after contact

    if env.continuous:
        a = np.array([hover_todo * 20 - 1, -angle_todo * 20])
        a = np.clip(a, -1, +1)
    else:
        a = 0
        if hover_todo > np.abs(angle_todo) and hover_todo > 0.05:
            a = 2
        elif angle_todo < -0.05:
            a = 4
        elif angle_todo > +0.05:
            a = 5
    return a

env = gym.make("RocketLander-v0", render_mode="human")
observation, info = env.reset()

display_surface = pygame.display.get_surface()
font = pygame.font.SysFont('ariel', 20)

terminated = False
truncated = False

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
            action = 5

        elif keys[pygame.K_d]:
            action = 4
        
        elif keys[pygame.K_LEFT]:
            action = 1
        
        elif keys[pygame.K_RIGHT]:
            action = 0
        
        else:
            action = 6
    
    else:
        try:
            action = np.argmax(net.activate(observation))

        except NameError:
            action = env.action_space.sample()
            print('OHO')

        except:
            print('Unknown ERROR')
    
    print(action)
    #action = heuristic(env, observation)
    #print(observation[1])
    #print(action)

    #action = 6 if action == 2 and steps < 190 else action

    # if 250 < steps < 300:
    #     time.sleep(1)

    observation, reward, terminated, truncated, info = env.step(action)
    
    #print(reward)

    total_reward += reward
    reward_per_step.append(reward)
    total_reward_per_step.append(total_reward)
    
    render_font(font, str(steps), display_surface)

    if terminated or truncated:
        print(steps)
        break
        runs += 1
        steps = 0
        observation, info = env.reset()

print(f"total_steps: {total_steps}, total_reward: {total_reward}")
display_stats(total_steps, reward_per_step, filename = os.path.join(local_dir, 'stats/fitness1.png'))
display_stats(total_steps, total_reward_per_step, filename = os.path.join(local_dir, 'stats/fitness2.png'))

env.close()