from config import *
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.y_offset = HITBOX_OFFSET[sprite_type]
        if sprite_type == 'object' or 'tree':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE//2))
        else:
            self.rect  = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, self.y_offset)