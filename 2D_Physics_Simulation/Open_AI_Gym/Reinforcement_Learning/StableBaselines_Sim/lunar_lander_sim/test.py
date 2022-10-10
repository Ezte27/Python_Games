import gym
from stable_baselines3 import A2C, PPO
import matplotlib.pyplot as plt
import warnings
import os
import numpy as np
from colorama import Fore

local_dir   = os.path.dirname(__file__)
models_dir  = "models"
model_name = input("Input the name of the folder and model [folder_name/model_num.zip]: ").strip(" ")
model_path = f"{models_dir}/{model_name}"

EPISODES    = 10

env = gym.make("LunarLander-v2")
observation = env.reset()

model = PPO.load(model_path, env=env)

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

for ep in range(EPISODES):
    observation = env.reset()
    done = False
    while not done:
        env.render()
        action, _ = model.predict(observation)
        observation, reward, done, info = env.step(action = action)

env.close()