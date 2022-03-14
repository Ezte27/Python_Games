from settings import *
from player import Player
from ball import Ball
from obstacle import Obstacle

import pygame, random

pygame.init()

SCORE_FONT = pygame.font.Font('consolas', 40)

class Main:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.player = Player((WIDTH//2, HEIGHT - 10), PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, PLAYER_SPEED)
        self.ball = Ball((self.player.x, self.player.y - BALL_RADIUS), BALL_RADIUS, BALL_COLOR, BALL_MAX_VEL)
        self.obstacles = []
        self.create_obtacles()

        self.clock = pygame.time.Clock()
        self.player_score = 0
        self.player_misses = 0
        self.player_hits = 0

        self.running = True

    def handle_collisions(self):
        if self.ball.y_vel < 0:
            for obstacle in self.obstacles:
                if (self.ball.x >= obstacle.x) and (self.ball.x <= obstacle.x + obstacle.width):
                    if self.ball.y - self.ball.radius <= obstacle.y + obstacle.height:
                        self.ball.y_vel *= -1
                        self.player_hits += 1

                        # middle_x = obstacle.x + self.player.width/2
                        # difference_in_x = middle_x - self.ball.x
                        # reduction_factor = (self.player.width/2) / self.ball.max_vel
                        # x_vel = difference_in_x / reduction_factor
                        #self.ball.x_vel = x_vel * -1
            
            if self.ball.y <= 0:
                self.restart_game(next_level=True)

        else:
            if (self.ball.x >= self.player.x) and (self.ball.x <= self.player.x + self.player.width):
                if self.ball.y + self.ball.radius >= self.player.y:
                    self.ball.y_vel *= -1
                    
                    # Some MATHS!
                    middle_x = self.player.x + self.player.width/2
                    difference_in_x = middle_x - self.ball.x
                    reduction_factor = (self.player.width/2) / self.ball.max_vel
                    x_vel = difference_in_x / reduction_factor
                    self.ball.x_vel = x_vel * -1
            elif self.ball.y >= HEIGHT:
                self.player_misses += 1
                self.restart_game()

    def create_obtacles(self):
        col_num = random.randint(WIDTH//85, WIDTH//50)
        for row in range(random.randint(2, 4)):
            for col in range(col_num):
                width = WIDTH//col_num
                height = OBSTACLE_HEIGHT
                pos = (col, row)
                color = random.choice(COLORS.remove(BLACK))
                self.obstacles.append(Obstacle(pos, width, height, color))
    
    def draw(self):
        player_score_text = SCORE_FONT.render(f'{self.player_score}', True, WHITE)

        self.win.fill(BLACK)
        self.win.blit(player_score_text, (WIDTH//2 - player_score_text.get_width()//2, 20))

        self.player.draw(self.win)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.win)
        
        self.ball.draw(self.win)

        pygame.display.update()

    def move_paddle(self, right=None):
        if not right and self.player.x > 0:
            self.player.move(right = False)
        elif right and self.player.x + self.player.width < WIDTH:
            self.player.move(right = True)

    def restart_game(self, next_level = False):
        if next_level:
            self.player_score += 1
            # self.obstacles = []
            # self.create_obtacles()
        else:
            pass

    def reset(self):
        self.player_score = 0
        self.player_hits = 0
        self.player_misses = 0
        self.obstacles = []
        self.create_obtacles()
        self.ball.reset()
        self.player.reset()

    def game_loop(self):
        self.clock.tick(FPS)
            
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_a]:
        #     self.move_paddle(right = False)
        # elif keys[pygame.K_d]:
        #     self.move_paddle(right = True)

        self.draw()  
        self.handle_collisions()
        self.ball.move() 