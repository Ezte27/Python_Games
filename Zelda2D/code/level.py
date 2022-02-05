import pygame
from config import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()
    
    def create_map(self):
        for index_row, row in enumerate(WORLD_MAP):
            for index_col, col in enumerate(row):
                x = index_col * TILESIZE
                y = index_row * TILESIZE
                if col == 'r':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.display_surface, self.player)
        self.visible_sprites.update()
        debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self): 
        super().__init__()
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self, display_surface, player):
        self.offset.x  = player.rect.centerx - WIDTH//2
        self.offset.y  = player.rect.centery - HEIGHT//2

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)