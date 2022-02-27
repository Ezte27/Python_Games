import time
import pygame
pygame.init()

WINDOW_NAME = 'PyPong'
WIDTH, HEIGHT = (700, 500)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_NAME)

PADDLE_WIDTH, PADDLE_HEIGHT = (20, 100)
BALL_RADIUS = 8

FPS = 60
WHITE = (255, 255, 255)
BLACK = (5, 5, 10)
PINK = (200, 100, 60)
BLUE = (50, 50, 220)
GRAY = (200, 200, 200)


class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 4
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

class Ball:
    def __init__(self, x, y, radius, color, max_vel = 5):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_vel = max_vel
        self.y_vel = 0
        self.max_vel = max_vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        if (self.y - self.radius <= 0) or (self.y + self.radius >= HEIGHT):
            self.y_vel *= -1
        self.x += self.x_vel
        self.y += self.y_vel

def handle_collisions(ball, left_paddle, right_paddle):
    if ball.x_vel < 0:
        if (ball.y >= left_paddle.y) and (ball.y <= left_paddle.y + left_paddle.height):
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2) / ball.max_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1
    else:
        if (ball.y >= right_paddle.y) and (ball.y <= right_paddle.y + right_paddle.height):
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2) / ball.max_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1


def draw(win, paddles, ball):
    win.fill(BLACK)
    for paddle in paddles:
        paddle.draw(win)
    
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 8, HEIGHT//20))
    
    ball.draw(win)

    pygame.display.update()

def paddle_movement(keys, right_paddle, left_paddle):
    if  keys[pygame.K_UP] and right_paddle.y > 0:
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height < HEIGHT:
        right_paddle.move(up = False)
    if  keys[pygame.K_w] and left_paddle.y > 0:
        left_paddle.move(up = True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height < HEIGHT:
        left_paddle.move(up = False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, BLUE)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PINK)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, GRAY)

    left_player_score = 0
    right_player_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        paddle_movement(keys, right_paddle, left_paddle)
        handle_collisions(ball, left_paddle, right_paddle)
        ball.move()

        if ball.x < 0:
            right_player_score += 1
            ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, GRAY)
            left_paddle.x, left_paddle.y = (10, HEIGHT//2 - PADDLE_HEIGHT//2)
            right_paddle.x, right_paddle.y = (WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
            time.sleep(2)
        elif ball.x > WIDTH:
            left_player_score += 1
            ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, GRAY,max_vel=-5)
            left_paddle.x, left_paddle.y = (10, HEIGHT//2 - PADDLE_HEIGHT//2)
            right_paddle.x, right_paddle.y = (WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
            time.sleep(2)

    pygame.quit()

if __name__ == '__main__':
    main()