import pygame
from pathlib import Path
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout, get_sprite
from random import choice
#from enemy import Enemy
#from upgrade_menu import Upgrade_menu

ground_layer_file_path = Path("map\map_ground_layer.csv").resolve().absolute()
race_track_layer_file_path = Path("map\map_race_track_layer.csv").resolve().absolute()
entities_layer_file_path = Path("map\map_entities_layer.csv").resolve().absolute()
border_layer_file_path = Path("map\map_border_layer.csv").resolve().absolute()

ground_tileset_file_path = Path("graphics/Background_Tiles/ground_tileset.png").resolve().absolute()
road_01_tileset_file_path = Path("graphics/Road_01/Road_01_tileset.png").resolve().absolute()

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.LayeredUpdates()

        self.clock = pygame.time.Clock()

        self.create_map()

        #self.upgrade_menu = Upgrade_menu(self.player)
        #self.game_paused = False
    
    def create_map(self):
        layouts = {
            'ground': import_csv_layout(ground_layer_file_path),
            'race_tracks': import_csv_layout(race_track_layer_file_path),
            'entities': import_csv_layout(entities_layer_file_path),
            'boundary': import_csv_layout(border_layer_file_path)
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '' and col != '0':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile(
                                (x,y),
                                [self.obstacle_sprites],
                                'boundary',
                                )
                        elif style == 'ground':
                            ground_sprite_pos = ((int(col) - 49) * TILESIZE, 0)
                            sprite = get_sprite(ground_tileset_file_path , ground_sprite_pos[0], ground_sprite_pos[1], TILESIZE, TILESIZE)
                            Tile(
                                (x,y),
                                [self.visible_sprites],
                                'ground',
                                sprite)

                        elif style == 'race_tracks':
                            track_id = int(col)
                            road_01_x = 0
                            road_01_y = 0
                            for road_row_index, road_row in enumerate(ROAD_TRACKS_01_POSITIONS):
                                for road_col_index, road_col in enumerate(road_row):
                                    if track_id == road_col:
                                        road_01_x = road_col_index
                                        road_01_y = road_row_index
                                        break
                            road_track_sprite_pos = (road_01_x * TILESIZE, road_01_y * TILESIZE)
                            sprite = get_sprite(road_01_tileset_file_path, road_track_sprite_pos[0], road_track_sprite_pos[1], TILESIZE, TILESIZE)
                            Tile(
                                (x,y),
                                [self.visible_sprites],
                                'tracks',
                                sprite)
                        
                        elif style == 'entities':
                            if col == '52':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites)
    def run(self):
        self.visible_sprites.custom_draw(self.player, self.obstacle_sprites)
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        self.clock.tick(FPS)

class YSortCameraGroup(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()

        # self.ground_surface = pygame.image.load('Zelda2D/assets/graphics/tilemap/ground.png')
        # self.ground_rect = self.ground_surface.get_rect(topleft = (0, 0))
    
    def custom_draw(self, player, obstacle_sprites):
        self.offset.x  = player.rect.centerx - WIDTH//2
        self.offset.y  = player.rect.centery - HEIGHT//2

        # self.ground_offset = self.ground_rect.topleft - self.offset
        # display_surface.blit(self.ground_surface, self.ground_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            sprite.rect.topleft -= self.offset
        for sprite in sorted(obstacle_sprites.sprites(), key = lambda sprite: sprite.rect.centery):
            sprite.rect.topleft -= self.offset