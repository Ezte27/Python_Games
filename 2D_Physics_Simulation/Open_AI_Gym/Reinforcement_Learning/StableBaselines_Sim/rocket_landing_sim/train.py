import gym
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.env_checker import check_env
import os, time
from colorama import Fore
import rocket_lander

local_dir  = os.path.dirname(__file__)
current_time = int(time.time())
models_dir = f"models/PPO-{current_time}"
log_dir    = f"logs/PPO-{current_time}"
TIMESTEPS  = 10000
NUM_RUNS   = 100

for path in [models_dir, log_dir]:
    if not os.path.exists(path):
        os.makedirs(path)

env = gym.make("RocketLander-v0")
observation = env.reset()

print("action space shape: ", env.action_space.shape)
print("observation space shape: ", env.observation_space.shape)

print("\nChecking Gym Environment ...")
check_env(env)

print(f"\nThe training has {Fore.GREEN}STARTED SUCCESSFULLY{Fore.RESET}")
starttime = time.time()

model = PPO("MlpPolicy", env, verbose = 1, tensorboard_log=log_dir)

for i in range(1, NUM_RUNS):
    model.learn(total_timesteps = TIMESTEPS, reset_num_timesteps = False, tb_log_name = "PPO")
    model.save(f"{local_dir}/{models_dir}/{TIMESTEPS*i}")

print(f"\nTraining done in: {Fore.LIGHTGREEN_EX}{round((((time.time() - starttime) / 60) / 60), ndigits=2)}hours{Fore.RESET}\n")

env.close()