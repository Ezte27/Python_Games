import os
# The settings file for Simple_NEAT_AI
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)
SCREEN_CAPTION = "I dont know what to name this program"
FPS = 120

CONFIG_PATH = f"{os.getcwd()}/config.txt"
MAX_GENERATIONS = 60
GENERATION_TIME = 7000 # In milliseconds

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_COLOR = 'Blue'

PREY_WIDTH  = 40
PREY_HEIGHT = 40
PREY_COLORS = ['Red']