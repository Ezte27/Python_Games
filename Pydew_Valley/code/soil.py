import pygame
import os
from settings import *
from support import *
from pytmx.util_pygame import load_pygame
from random import choice

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water']

class SoilLayer:
    def __init__(self, all_sprites) -> None:
        
        # Sprite Groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surfs = import_folder_dict("graphics/soil")
        self.water_surfs = import_folder("graphics/soil_water")

        self.create_soil_grid()
        self.hitBoxes = []
        self.create_hitBoxes()

    def create_soil_grid(self):
        ground = pygame.image.load(os.path.join("graphics/world", "ground.png"))
        horizontal_tiles, vertical_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(horizontal_tiles)] for row in range(vertical_tiles)]
        for x, y, _ in load_pygame(os.path.join("data", "map.tmx")).get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append("F")
    
    def create_hitBoxes(self):
        self.hitBoxes = []
        for row_index, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "F" in cell:
                    x = index_col * TILE_SIZE
                    y = row_index * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hitBoxes.append(rect)
    
    def get_hit(self, point):
        for rect in self.hitBoxes:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X') # X = Soil patch in tile
                    self.create_soil_tiles()
    
    def water(self, point):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(point):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append("W")

                WaterTile((soil_sprite.rect.topleft), choice(self.water_surfs), [self.all_sprites, self.water_sprites])
    
    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()
        
        for row in self.grid:
            for cell in row:
                if "W" in cell:
                    cell.remove('W')

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    # Tile Options
                    t = 'X' in self.grid[index_row - 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]
                    b = 'X' in self.grid[index_row + 1][index_col]

                    # Tile Type
                    tile_type = 'o'
                    if all((t, r, l, b)): tile_type = 'x' # all() for checking True values in a tuple or list
                    
                    # Horizontal tiles
                    if l and not any((t,r,b)): tile_type = 'r'
                    if r and not any((t,l,b)): tile_type = 'l'
                    if l and r and not any((t,b)): tile_type = 'lr'
                    
                    # Vertical tiles
                    if t and not any((l,r,b)): tile_type = 'b'
                    if b and not any((t,r,l)): tile_type = 't'
                    if t and b and not any((l,r)): tile_type = 'tb'

                    # Corner tiles
                    if r and t and not any((l,b)): tile_type = 'bl'
                    if r and b and not any((l,t)): tile_type = 'tl'
                    if l and t and not any((r,b)): tile_type = 'br'
                    if l and b and not any((r,t)): tile_type = 'tr'

                    # T-Shape Tiles
                    if all((t,b,r)) and not l: tile_type = "tbr"
                    if all((t,b,l)) and not r: tile_type = "tbl"
                    if all((l, r,t)) and not b: tile_type = "lrb"
                    if all((l, r,b)) and not t: tile_type = "lrt"

                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE), self.soil_surfs[tile_type], [self.all_sprites, self.soil_sprites])
