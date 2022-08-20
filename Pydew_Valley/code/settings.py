from pygame.math import Vector2

# General
TOOLS = ['hoe', 'axe', 'water'] # All the tools available in the game (not necessarily the player tools)
SEEDS = ['corn', 'tomato'] # All the seeds available in the game

# Screen
SCREEN_WIDTH = 800#1366
SCREEN_HEIGHT = 600#768
SCREEN_CAPTION = 'PYDEW VALLEY'
TILE_SIZE = 64

# Player Attributes
PLAYER_SPEED = 150

# Overlay positions

OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50),
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10,
}