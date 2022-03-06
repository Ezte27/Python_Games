import time
import pygame
from settings import *
from ball import Ball
from paddle import Paddle
pygame.init()
SCORE_FONT = pygame.font.SysFont('ariel', 50)
GAME_FONT = pygame.font.SysFont('consolas', 50)

class Game:
    def __init__(self, win, ai=False):
        self.running = True
        self.clock = pygame.time.Clock()
        self.win = win
        self.ai = ai

        self.left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PINK)
        self.right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, BLUE)
        self.ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, GRAY)

        self.left_player_score = 0
        self.right_player_score = 0

        self.left_player_hits = 0
        self.right_player_hits = 0

        self.left_player_misses = 0
        self.right_player_misses = 0

        self.paddles = [self.left_paddle, self.right_paddle]

    def handle_collisions(self):
        if self.ball.x_vel < 0:
            if (self.ball.y >= self.left_paddle.y) and (self.ball.y <= self.left_paddle.y + self.left_paddle.height):
                if self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
                    self.ball.x_vel *= -1
                    self.left_player_hits += 1

                    middle_y = self.left_paddle.y + self.left_paddle.height/2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = (self.left_paddle.height/2) / self.ball.max_vel
                    y_vel = difference_in_y / reduction_factor
                    self.ball.y_vel = y_vel * -1
        else:
            if (self.ball.y >= self.right_paddle.y) and (self.ball.y <= self.right_paddle.y + self.right_paddle.height):
                if self.ball.x + self.ball.radius >= self.right_paddle.x:
                    self.ball.x_vel *= -1
                    self.right_player_hits += 1

                    middle_y = self.right_paddle.y + self.right_paddle.height/2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = (self.right_paddle.height/2) / self.ball.max_vel
                    y_vel = difference_in_y / reduction_factor
                    self.ball.y_vel = y_vel * -1

    def draw(self):
        self.win.fill(BLACK)
        if not self.ai:
            left_score_text = SCORE_FONT.render(f'{self.left_player_score}', True, WHITE)
            right_score_text = SCORE_FONT.render(f'{self.right_player_score}', True, WHITE)
            self.win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
            self.win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))
        else:
            left_hits_text = SCORE_FONT.render(f'{self.left_player_hits}', True, WHITE)
            right_hits_text = SCORE_FONT.render(f'{self.right_player_hits}', True, WHITE)
            self.win.blit(left_hits_text, (WIDTH//4 - left_hits_text.get_width()//2, 20))
            self.win.blit(right_hits_text, (WIDTH * (3/4) - right_hits_text.get_width()//2, 20))
        
        for paddle in self.paddles:
            paddle.draw(self.win)
        
        for i in range(10, HEIGHT, HEIGHT//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win, WHITE, (WIDTH//2 - 5, i, 8, HEIGHT//20))
        
        self.ball.draw(self.win)

        pygame.display.update()

    # def paddle_movement(self, keys):
    #     if  keys[pygame.K_UP] and self.right_paddle.y > 0:
    #         self.right_paddle.move(up = True)
    #     if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.height < HEIGHT:
    #         self.right_paddle.move(up = False)
    #     if  keys[pygame.K_w] and self.left_paddle.y > 0:
    #         self.left_paddle.move(up = True)
    #     if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.height < HEIGHT:
    #         self.left_paddle.move(up = False)
    
    def move_paddle(self, left=True, up=None):
        if not left and self.right_paddle.y > 0 and up:
            self.right_paddle.move(up = True)
        if not left and self.right_paddle.y + self.right_paddle.height < HEIGHT and not up:
            self.right_paddle.move(up = False)
        if left and up and self.left_paddle.y > 0:
            self.left_paddle.move(up = True)
        if left and not up and self.left_paddle.y + self.left_paddle.height < HEIGHT:
            self.left_paddle.move(up = False)
    
    def check_win(self, player_score):
        if player_score >= 10:
            time.sleep(1) if not self.ai else None
            self.win.fill(BLACK)
            text = 'RIGHT' if self.right_player_score >= 10 else 'LEFT'
            if not self.ai:
                win_text = GAME_FONT.render(f'{text} PLAYER WON!!', True, BLUE)
                self.win.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            time.sleep(4) if not self.ai else None
            self.running = False
    
    def restart_game(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        time.sleep(.8) if not self.ai else None

    def reset(self):
        self.left_player_score = 0
        self.right_player_score = 0
        self.left_player_hits = 0
        self.right_player_hits = 0
        self.left_player_misses = 0
        self.right_player_misses = 0
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()

    def loop(self):
        self.clock.tick(FPS)
        if not self.ai:
            self.draw()  
        self.move_paddle()
        self.handle_collisions()
        self.ball.move()
        self.check_win(self.right_player_score)
        self.check_win(self.left_player_score)
        
        if self.ball.x < 0:
            self.right_player_score += 1
            self.left_player_misses += 1
            self.restart_game()
        elif self.ball.x > WIDTH:
            self.left_player_score += 1
            self.right_player_misses += 1
            self.restart_game()