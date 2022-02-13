import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect  = self.image.get_rect(topleft = pos)
        if self.sprite_type == 'boundary':
            self._layer = 1
        elif self.sprite_type == 'ground':
            self._layer = 2
        elif self.sprite_type == 'tracks':
            self._layer = 3