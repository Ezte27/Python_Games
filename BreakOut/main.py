from settings import *
from player import Player
from ball import Ball
from obstacle import Obstacle

import pygame, random

pygame.init()

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.player = Player((WIDTH//2, HEIGHT - 10), PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, PLAYER_SPEED)
        self.ball = Ball((self.player.x, self.player.y - BALL_RADIUS), BALL_RADIUS, BALL_COLOR, BALL_MAX_VEL)
        self.obstacles = []
        self.create_obtacles()

        self.clock = pygame.time.Clock()
        self.player_score = 0

    def handle_collisions(self):
        pass

    def create_obtacles(self):
        col_num = random.randint(WIDTH//85, WIDTH//50)
        for row in range(random.randint(2, 4)):
            for col in range(col_num):
                width = WIDTH//col_num
                height = OBSTACLE_HEIGHT
                pos = (col, row)
                color = random.choice(COLORS.remove(BLACK))
                self.obstacles.append(Obstacle(pos, width, height, color))
    
    def game_loop(self):
        pass