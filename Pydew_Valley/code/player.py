import pygame
import pathlib
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group) -> None:
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # General Setup
        self.image = self.animations[self.status][self.frame_index] # image surface for sprites, it is used by pygame.sprite.Sprite
        self.rect = self.image.get_rect(center = pos)

        # Movement Attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED
    
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'right': [], 'left': [],
                           'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': [], 
                           'up_hoe': [], 'down_hoe': [], 'right_hoe': [], 'left_hoe': [], 
                           'up_axe': [], 'down_axe': [], 'right_axe': [], 'left_axe': [], 
                           'up_water': [], 'down_water': [], 'right_water': [], 'left_water': [], }

        for animation in self.animations.keys():
            full_path = pathlib.Path('../assets/character/' + animation).resolve().absolute()
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, dt):

        # normalizing a vector to ensure that the speed is always constant
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
        
    def update(self, dt):
        self.input()
        self.move(dt)