import pygame
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout, get_sprite
from random import choice
#from enemy import Enemy
#from upgrade_menu import Upgrade_menu

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.create_map()

        #self.upgrade_menu = Upgrade_menu(self.player)
        #self.game_paused = False
    
    def create_map(self):
        layouts = {
            'ground': import_csv_layout('2D_Racing_Game\map\map_ground_layer.csv'),
            'race_tracks': import_csv_layout('2D_Racing_Game\map\map_race_track_layer.csv'),
            'entities': import_csv_layout('2D_Racing_Game\map\map_entities_layer.csv'),
            'boundary': import_csv_layout('2D_Racing_Game\map\map_border_layer.csv')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile(
                                (x,y),
                                [self.obstacle_sprites],
                                'boundary'
                                )
                        elif style == 'ground':
                            ground_sprite_pos = ((int(col) - 49) * TILESIZE, 0)
                            sprite = get_sprite('2D_Racing_Game/graphics/Road_01/Road_01_tileset.png', ground_sprite_pos[0], ground_sprite_pos[1], TILESIZE, TILESIZE)
                            Tile(
                                (x,y),
                                [self.visible_sprites],
                                'ground',
                                sprite)

                        elif style == 'race_tracks':
                            if int(col) - 1 <= 7:
                                road_track_sprite_pos_y = 0
                            elif 7 < int(col) - 1 <= 15:
                                road_track_sprite_pos_y = 1
                            elif 15 < int(col) - 1 <= 23:
                                road_track_sprite_pos_y = 2
                            elif 23 < int(col) - 1 <= 31:
                                road_track_sprite_pos_y = 3
                            elif 31 < int(col) - 1 <= 39:
                                road_track_sprite_pos_y = 4
                            elif 39 < int(col) - 1 <= 47:
                                road_track_sprite_pos_y = 5
                            else:
                                print('ERROR! -- Location = file: level.py / line: 81')
                                print('Road_Track_Sprite y_pos NOT-FOUND')
                                print('----------------------------------------------')
                                pygame.quit()
                            road_track_sprite_pos = ((int(col) - 1) * TILESIZE, road_track_sprite_pos_y)
                            sprite = get_sprite('2D_Racing_Game/graphics/Road_01/Road_01_tileset.png', road_track_sprite_pos[0], road_track_sprite_pos[1], TILESIZE, TILESIZE)
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
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        self.clock.tick(FPS)