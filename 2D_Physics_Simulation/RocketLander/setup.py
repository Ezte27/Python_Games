from setuptools import setup

setup(name='rocket_lander',
      version='0.1',
      url='https://github.com/Jeetu95/Rocket_Lander_Gym',
      author='Esteban Calderon',
      author_email='estedcg27@gmail.com',
      description='Open Ai Gym Environment for a Rocket Lander Simulation',
      license='MIT',
      packages=['envs'],
      install_requires=['gym','numpy', 'pygame']
      )