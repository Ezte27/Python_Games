import os
from colorama import Fore
import gym
from Rocket_Lander_Gym.rocket_lander_gym.envs import rocket_lander
import numpy as np

env = gym.make("RocketLander-v0", render_mode = 'human', gravity = -50)

observation, info = env.reset()

print(env.action_space)
local_dir = os.path.dirname(__file__)
neat_sim_dir = os.path.split(os.path.split(local_dir)[0])[0]
print(f"{Fore.BLUE}{neat_sim_dir}{Fore.RESET}")

terminated = False
truncated = False

steps = 0
runs = 0
while runs < 1:

    action = env.action_space.sample() #np.argmax([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    observation, reward, terminated, truncated, info = env.step(action)

    print(reward)

    steps += 1

    if steps > 30:
        terminated = True

    if terminated or truncated:
        observation, info = env.reset()
        runs += 1

env.close()