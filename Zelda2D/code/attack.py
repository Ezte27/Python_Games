from msilib.schema import Directory
import pygame
from config import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.direction = player.status.split('_')[0]

        #graphics
        full_path = f'Zelda2D/assets/graphics/weapons/{player.weapon}/{self.direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        #placement
        if self.direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, TILESIZE//4))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, TILESIZE//4))
        elif self.direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        elif self.direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)

class Fist(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'fist'
        self.direction = player.status.split('_')[0]

        #graphics
        self.image = pygame.Surface((40, 40))

        #placement
        if self.direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, TILESIZE//4))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, TILESIZE//4))
        elif self.direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        elif self.direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)
