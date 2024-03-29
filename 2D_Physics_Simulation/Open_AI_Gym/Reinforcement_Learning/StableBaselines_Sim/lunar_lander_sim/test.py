from time import sleep, time
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

EPISODES      = 5
TEST_ACCURACY = True

env = gym.make("LunarLander-v2")
observation = env.reset()

model = PPO.load(model_path, env=env)

def display_stats(steps:int, reward_per_step: list, view:bool = True, ylog:bool = False, filename:str ='stats/fitness.svg'):
    if plt is None:
        warnings.warn("This display is unavailable due to missing dependency (matplotlib)")
    frames = range(steps)
    fitness = np.array(reward_per_step)

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

landings = 0
accuracy = 0
keywords = ['awful', 'acceptable', 'outstanding']

if TEST_ACCURACY:
    print(f"The testing has {Fore.GREEN}STARTED SUCCESSFULLY{Fore.RESET}")
    starttime = time()

for ep in range(EPISODES):
    observation = env.reset()
    done = False
    while not done:
        if TEST_ACCURACY:
            env.render()
        action, _ = model.predict(observation)
        observation, reward, done, info = env.step(action = action)

        if reward == +100 and done:
            landings += 1

if TEST_ACCURACY:
    print(f"Testing done in: {Fore.LIGHTGREEN_EX}{round(time() - starttime, ndigits=2)} secs{Fore.RESET}")
    sleep(2.5)

accuracy = (landings / EPISODES)
print(f"The model landed successfully {Fore.CYAN}{landings}{Fore.RESET} over a total of {Fore.GREEN}{EPISODES}{Fore.RESET} landing attempts.")
print(f"The model had an {Fore.LIGHTBLUE_EX}{keywords[0] if accuracy < 0.4 else keywords[1] if 0.4 < accuracy < 0.8 else keywords[2]} accuracy{Fore.RESET} of {Fore.GREEN}{round(accuracy * 100, ndigits=2)}%{Fore.RESET}")

env.close()