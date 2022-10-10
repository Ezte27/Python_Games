import gym
from stable_baselines3 import A2C, PPO
import os

local_dir   = os.path.dirname(__file__)
models_dir  = "models/PPO"
model_path = f"{models_dir}/20000.zip"
log_dir     = "logs"
EPISODES    = 10

env = gym.make("LunarLander-v2")
observation = env.reset()

model = PPO.load(model_path, env=env)

for ep in range(EPISODES):
    observation = env.reset()
    done = False
    while not done:
        env.render()
        action, _ = model.predict(observation)
        observation, reward, done, info = env.step(action = action)

env.close()