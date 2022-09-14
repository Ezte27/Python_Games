import gym
from pygame.time import Clock

env = gym.make("LunarLander-v2", render_mode="human")

observation = env.reset()

print(observation)
print(env.action_space)

clock = Clock()
FPS = 50

terminated = False
truncated = False
for _ in range(1000):
    clock.tick(FPS)

    observation, reward, terminated, truncated, info = env.step(env.action_space.sample())

    if terminated or truncated:
        observation, info = env.reset()

env.close()