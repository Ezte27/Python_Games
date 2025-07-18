import time
import gym
from stable_baselines3 import A2C, PPO
import os
from colorama import Fore
import rocket_lander

local_dir   = os.path.dirname(__file__)
models_dir  = "models"
model_name = input("Input the name of the folder and model [folder_name/model_num.zip]: ").strip(" ")
model_path = f"{models_dir}/{model_name}"

EPISODES      = 15
TEST_ACCURACY = False

env = gym.make("RocketLander-v0", render_mode = 'human')
observation = env.reset()

model = PPO.load(model_path, env=env)

landings = 0
accuracy = 0
keywords = ['awful', 'acceptable', 'outstanding']

if TEST_ACCURACY:
    print(f"The testing has {Fore.GREEN}STARTED SUCCESSFULLY{Fore.RESET}")
    starttime = time.time()

for ep in range(EPISODES):
    observation = env.reset()
    done = False
    while not done:
        action, _ = model.predict(observation)
        observation, reward, done, info = env.step(action = action)

        if reward >= 230 and done:
            landings += 1

if TEST_ACCURACY:
    print(f"Testing done in: {Fore.LIGHTGREEN_EX}{round(time.time() - starttime, ndigits=2)} secs{Fore.RESET}")
    time.sleep(2.5)

accuracy = (landings / EPISODES)
print(f"The model landed successfully {Fore.CYAN}{landings}{Fore.RESET} over a total of {Fore.GREEN}{EPISODES}{Fore.RESET} landing attempts.")
print(f"The model had an {Fore.LIGHTBLUE_EX}{keywords[0] if accuracy < 0.4 else keywords[1] if 0.4 < accuracy < 0.9 else keywords[2]} accuracy{Fore.RESET} of {Fore.GREEN}{round(accuracy * 100, ndigits=2)}%{Fore.RESET}")

env.close()