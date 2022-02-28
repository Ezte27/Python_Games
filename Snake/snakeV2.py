import pygame, sys, random
from pygame.math import Vector2

# VARIABLES
WHITE = (255, 255, 255)
GREEN = (175,214,70)
DARK_GREEN = (139,189,30)
BLUE = (25, 60, 250)
DARK_BLUE = (0,18,35)
RED = (250, 40, 50)
BLACK = (0, 0, 0)

cell_size = 30
cell_number = 20

WIN_WIDTH = (cell_number * cell_size)
WIN_HEIGHT = (cell_number * cell_size)
GAME_SPEED = 150 #Miliseconds
FPS = 60


# END VARIABLES

class FRUIT():
    def __init__(self):
        self.image = pygame.image.load('Snake/img/apple.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.randomize()
        self.rect.x, self.rect.y = (self.x_pos * cell_size, self.y_pos * cell_size)

    def draw_fruit(self):
        screen.blit(self.image, self.rect)
    
    def randomize(self):
        self.x_pos = random.randint(0, cell_number - 1)
        self.y_pos = random.randint(0, cell_number - 1)
        self.pos = (self.x_pos, self.y_pos)

class SNAKE():
    def __init__(self):
        self.original_body = [Vector2(10,10), Vector2(10, 11)]
        self.body = self.original_body
        self.direction = Vector2(1,0)
        self.animation_index = cell_size
        self.animation_speed = .1

    def draw_snake(self):
        self.animate_snake()
        # for block in self.body:
        #     block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
        #     pygame.draw.rect(screen, BLUE, block_rect)
    
    def animate_snake(self):
        self.animation_index -= self.animation_speed
        for block in self.body:
            block_rect = pygame.Rect(int(block.x * (cell_size)), int(block.y * (cell_size)), cell_size, cell_size)
            pygame.draw.rect(screen, BLUE, block_rect)
        if self.animation_index <= 0:
            self.animation_index = cell_size

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def add_block(self):
        self.block_x = self.body[-1].x
        self.block_y = self.body[-1].y
        self.body.append(Vector2(self.block_x, self.block_y))

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.lost = False

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def drawElements(self):
        if self.lost:
            self.game_over()
        else:
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            print('Snack')
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.lost = True
        if not 0 <= self.snake.body[0].y < cell_number:
            self.lost = True
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.lost = True
    def game_over(self):
        screen.fill(DARK_BLUE)
        self.game_over_text = 'YOU LOST'
        self.game_over_text_surface = game_over_font.render(self.game_over_text, True, RED)
        self.game_over_rect = self.game_over_text_surface.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2 - 150))
        self.score_rect = self.score_surface.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2 - 80))
        screen.blit(self.game_over_text_surface, self.game_over_rect)
        screen.blit(self.score_surface, self.score_rect)
        button1.update()
        button2.update()
        

    def draw_grass(self):
        grass_color = GREEN

        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, GREEN, grass_rect)
            else:
                for column in range(cell_number):
                    if column % 2 != 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, GREEN, grass_rect)
    
    def draw_score(self):
        self.score_text = f'Score: {len(self.snake.body) - 2}'
        self.score_surface = game_font.render(self.score_text, True, (56, 74, 12))
        score_x = WIN_WIDTH - 40
        score_y = 20
        self.score_rect = self.score_surface.get_rect(topright= (score_x, score_y))
        screen.blit(self.score_surface, self.score_rect)
        
class Button:
    def __init__(self, text, width, height, pos, color, radius, overlapColor, bColor, function,elevation=6):
        self.pressed = False
        self.original_elevation = elevation
        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.function = function

        self.top_rect = pygame.Rect((pos), (width, height))
        self.color = color
        self.overlapcolor = overlapColor
        self.top_color = self.color
        self.radius = radius

        self.bottom_rect = pygame.Rect(pos, (width, self.elevation))
        self.bottom_color = bColor

        self.text_surf = game_font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def update(self):
        self.draw()
        self.check_click()

    def draw(self):
        self.top_rect.y = self.original_y_pos - self.elevation
        self.text_rect.center = self.top_rect.center

        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=self.radius)
        screen.blit(self.text_surf, self.text_rect)
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.overlapcolor
            if pygame.mouse.get_pressed()[0]:
                self.elevation = 0
                self.pressed = True
            else:
                if self.pressed:
                    if self.function == 'quit':
                        pygame.quit()
                        sys.exit()
                    elif self.function == 'playagain':
                        main_game.snake.body = main_game.snake.original_body
                        main_game.lost = False
                        
                    print('Click')
                    self.pressed = False
                self.elevation = self.original_elevation
        else:
            self.elevation = self.original_elevation
            self.top_color = self.color

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
game_font = pygame.font.Font('OSRS_python/Gamefonts/Roboto-Medium.ttf', 25)
game_over_font = pygame.font.Font('OSRS_python/Gamefonts/Roboto-Medium.ttf', 60)
button1 = Button('EXIT', 180, 40, (WIN_WIDTH/2 + 20, WIN_HEIGHT/2), RED, 14, (255, 165, 10), BLACK, 'quit')
button2 = Button('PLAY AGAIN', 180, 40, (WIN_WIDTH/2 - 200, WIN_HEIGHT/2), (20, 250, 30), 14, BLUE, BLACK, 'playagain')

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, GAME_SPEED)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if main_game.lost != True:
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

    if main_game.lost != True:
        screen.fill(DARK_GREEN)
    main_game.drawElements()
    pygame.display.update()
    clock.tick(FPS)