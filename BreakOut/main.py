from settings import *
from player import Player
from ball import Ball
from obstacle import Obstacle

import pygame, random, time

pygame.init()

SCORE_FONT = pygame.font.SysFont('consolas', 40)
LEVEL_FONT = pygame.font.SysFont('consolas', 20)

class Main:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.player = Player((WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - PLAYER_HEIGHT*3), PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, PLAYER_SPEED)
        self.ball = Ball((self.player.rect.centerx, self.player.rect.centery - BALL_RADIUS - self.player.height//2), BALL_RADIUS, BALL_COLOR, BALL_MAX_VEL)
        self.obstacles = []
        self.create_obtacles()

        self.clock = pygame.time.Clock()
        self.player_score = 0
        self.player_misses = 0

        self.level = 1

    def handle_ball_collisions(self):

        for obstacle in self.obstacles:
            if self.ball.rect.colliderect(obstacle.rect):
                if abs(obstacle.rect.top - self.ball.rect.bottom) < 8:
                    self.ball.y_vel *= -1
                    self.player_score += 1
                    self.obstacles.remove(obstacle)
                    del obstacle
                
                elif abs(obstacle.rect.bottom - self.ball.rect.top) < 8:
                    self.ball.y_vel *= -1
                    self.player_score += 1
                    self.obstacles.remove(obstacle)
                    del obstacle
                
                elif abs(obstacle.rect.left - self.ball.rect.right) < 8:
                    self.ball.x_vel *= -1
                    self.player_score += 1
                    self.obstacles.remove(obstacle)
                    del obstacle
                
                elif abs(obstacle.rect.right - self.ball.rect.left) < 8:
                    self.ball.x_vel *= -1
                    self.player_score += 1
                    self.obstacles.remove(obstacle)
                    del obstacle

        if self.ball.y_vel < 0: 
            if self.ball.y - self.ball.radius <= 0:
                self.ball.y_vel *= -1

        elif self.ball.y_vel > 0:
            if self.player.rect.colliderect(self.ball.rect):
                self.ball.y_vel *= -1
                   
                # Some MATHS for paddle and ball collision!
                middle_x = self.player.x + self.player.width/2
                difference_in_x = middle_x - self.ball.x
                reduction_factor = (self.player.width/2) / self.ball.max_vel
                x_vel = difference_in_x / reduction_factor
                self.ball.x_vel = x_vel * -1

            if self.ball.y >= HEIGHT:
                self.restart_game()
                


    def create_obtacles(self):
        height_offset = random.randint(45, 85)
        for row in range(random.randint(2, 4)):
            col_num = random.choice([WIDTH//80, WIDTH//40])
            for col in range(col_num):
                width = WIDTH//col_num
                height = OBSTACLE_HEIGHT
                pos = (col * width, row * height + height_offset)
                color = random.choice(OBSTACLE_COLORS)
                self.obstacles.append(Obstacle(pos, width, height, color))
    
    def draw(self):
        player_score_text = SCORE_FONT.render(f'{self.player_score}', True, WHITE)
        level_text = LEVEL_FONT.render(f'Level: {self.level}', True, GRAY)

        self.win.fill(BLACK)
        self.win.blit(player_score_text, (WIDTH//2 - player_score_text.get_width()//2, 20))
        self.win.blit(level_text, (WIDTH - level_text.get_width() - WIDTH//30 , 20))

        self.player.draw(self.win)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.win)
        
        self.ball.draw(self.win)

        pygame.display.update()

    def move_paddle(self, right=None):
        if not right and self.player.rect.x > 0:
            self.player.move(right = False)
        elif right and self.player.rect.x + self.player.rect.width < WIDTH:
            self.player.move(right = True)

    def restart_game(self, next_level = False):
        if next_level:
            self.level += 1
            self.obstacles = []
            self.create_obtacles()
            self.ball.reset()
            self.player.reset()
            time.sleep(NEXT_LEVEL_DELAY)

        else:
            self.player_misses += 1
            self.ball.reset()
            self.player.reset()
            time.sleep(MISSED_THE_BALL_DELAY)

    def reset(self):
        self.player_score = 0
        self.player_hits = 0
        self.obstacles = []
        self.create_obtacles()
        self.ball.reset()
        self.player.reset()
    
    def check_win(self):
        if len(self.obstacles) == 0:
            self.restart_game(next_level=True)

    def game_loop(self):
        self.clock.tick(FPS)
            
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_a]:
        #     self.move_paddle(right = False)
        # elif keys[pygame.K_d]:
        #     self.move_paddle(right = True)

        self.draw()  
        self.handle_ball_collisions()
        self.ball.move() 