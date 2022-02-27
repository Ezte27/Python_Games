import math
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.image = pygame.image.load('2D_Racing_Game\graphics\Cars\yellow_car.png').convert_alpha()
        self.rect  = self.image.get_rect(topleft = pos)
        self.rect = self.rect.inflate(HITBOX_OFFSET[0], HITBOX_OFFSET[1])
        self._layer = 4

        self.obstacles = obstacles

        # movement

        self.max_speed = PLAYER_SPEED
        self.velocity = 0
        self.acceleration = 0
        self.direction = pygame.math.Vector2()
        
           
    def input(self):
        keys_pressed = pygame.key.get_pressed()

        #Movement Input
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.direction.y = -1
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.direction.x = -1

        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.direction.x = 1

        else:
            self.direction.x = 0
    
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
    
    def animate_player(self):
        pass
    
    def update(self):
        self.input()
        self.move()
        #self.animate_player()