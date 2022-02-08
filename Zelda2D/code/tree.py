import pygame

from config import *

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = surface
        self.current_attack = None
        self.y_offset = HITBOX_OFFSET['tree']
        self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE//2))
        self.hitbox = self.rect.inflate(0, self.y_offset)
        self.health = TREE_HEALTH