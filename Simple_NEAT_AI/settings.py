import os
# The settings file for Simple_NEAT_AI
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)
SCREEN_CAPTION = "I dont know what to name this program"
FPS = 120

CONFIG_PATH = f"{os.getcwd()}/config.txt"
MAX_GENERATIONS = 600
GENERATION_TIME = 7000 # In milliseconds

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_COLOR = 'Blue'

PREY_WIDTH  = 40
PREY_HEIGHT = 40
PREY_COLORS = ['Red']

#               -Red        - Yellow       - Green       - Cyan        - Blue       - Purple
BG_COLORS = [(200, 0, 0), (200, 200, 0), (0, 200, 0), (0, 200, 200), (0, 0, 200), (160, 32, 240)]
BG_COLORS.extend([(255,0,255), (192,192,192), (128,128,128), (128,0,0), (128,128,0), (0,128,0), (165,42,42), (255,99,71), (255,165,0), (0,139,139), (0,206,209), ])
COLOR_CHANGES_NUM = 3
COLOR_DURATION = 3500