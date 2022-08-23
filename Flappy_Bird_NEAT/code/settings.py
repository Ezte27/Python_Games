import pygame
import os

# Screen config
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 710
SCREEN_CAPTION = 'Flappy Bird With NEAT'
FPS = 30

# Images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('assets\Player', 'bird1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('assets\Player', 'bird2.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('assets\Player', 'bird3.png')))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets\Environment', 'pipe.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets\Environment', 'base.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets\Environment', 'bg.png')))

# Player
MAX_ROTATION = 25
ROT_VEL = 20
ANIMATION_TIME = 2

# Pipe
GAP = 200
PIPE_VEL = 5
PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
PIPE_BOTTOM = PIPE_IMG

# Base
BASE_VEL = 5
BASE_WIDTH = BASE_IMG.get_width()