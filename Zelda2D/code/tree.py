from config import *
import pygame

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = surface
        self.sprite_type = 'tree'
        self.current_attack = None
        self.y_offset = HITBOX_OFFSET['tree']
        self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE//2))
        self.hitbox = self.rect.inflate(0, self.y_offset)
        self.health = TREE_HEALTH
    def check_death(self):
        if self.health <= 0:
            self.kill()
    def chop(self, damage, current_player_attack):
        if self.current_attack != current_player_attack:
            self.health -= damage
            self.current_attack = current_player_attack
    def update(self):
        self.check_death()