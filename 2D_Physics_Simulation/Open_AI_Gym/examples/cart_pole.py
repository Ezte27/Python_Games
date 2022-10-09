import gym

env = gym.make("CartPole-v1", render_mode="human")

observation = env.reset()

print(observation)
print(env.action_space)

terminated = False
truncated = False
for _ in range(1000):
    observation, reward, terminated, truncated, info = env.step(env.action_space.sample())
    print(env.action_space.sample())

    if terminated or truncated:
        observation, info = env.reset()

env.close()