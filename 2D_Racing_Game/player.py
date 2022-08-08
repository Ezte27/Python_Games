import math
import pygame
from pathlib import Path
from settings import *

car_file_path = Path("graphics\Cars\yellow_car.png").resolve().absolute()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.original_image = pygame.image.load(car_file_path).convert_alpha()
        self.image = self.original_image
        self.rect  = self.image.get_rect(topleft = pos)
        self.rect = self.rect.inflate(HITBOX_OFFSET[0], HITBOX_OFFSET[1])
        self.angle = 0
        self.x_vel = 0
        self.y_vel = 0
        self.velocity = 0
        self._layer = 4

        self.obstacles = obstacles

        # movement

        self.max_speed = PLAYER_SPEED
        self.acceleration = 0
        self.direction = pygame.math.Vector2()

    def input(self):
        keys_pressed = pygame.key.get_pressed()

        #Movement Input
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.velocity = self.max_speed
            self.direction.y = -1
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.velocity = 0
            self.direction.y = 0

        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.angle += 2.5

        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.angle -= 2.5

        else:
            self.direction.x = 0
    
    def find_quadrant(self):
        a = self.angle
        while not 0 <= a < 360:
            if a >= 360:
                a -= 360

            elif a < 0:
                a += 360
        
        return (a//90) + 1

    def move(self):
        self.x_vel = self.velocity * math.cos(self.angle * math.pi/180)
        self.y_vel = self.velocity * math.sin(self.angle * math.pi/180)

        self.rect.x += self.x_vel
        self.rect.y -= self.y_vel

        self.collision('horizontal')
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

    def rotate(self):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        self.input()
        self.move()
        self.rotate()
        #self.animate_player()