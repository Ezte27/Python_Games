import pygame
from attack import Weapon, Fist
from config import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder
from random import choice
from ui import UI
from tree import Tree
from enemy import Enemy
from upgrade_menu import Upgrade_menu

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.create_map()

        self.ui = UI()
        self.upgrade_menu = Upgrade_menu(self.player)
        self.game_paused = False
    
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('Zelda2D\map\map_FloorBlocks.csv'),
            'grass': import_csv_layout('Zelda2D\map\map_Grass.csv'),
            'object': import_csv_layout('Zelda2D\map\map_Objects.csv'),
            'entities': import_csv_layout('Zelda2D\map\map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('Zelda2D/assets/graphics/grass'),
            'objects': import_folder('Zelda2D/assets/graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile(
                                (x,y),
                                [self.obstacle_sprites],
                                'invisible'
                                )
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x,y),
                                [self.visible_sprites,self.attackable_sprites,self.obstacle_sprites],
                                'grass',
                                random_grass_image)

                        elif style == 'object':
                            if col != '2' and col != '3' and col != '4' and col != '5' and col != '6' and col != '7':
                                surf = graphics['objects'][int(col)]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
                            elif col == '2' or col == '3' or col == '4' or col == '5' or col == '6' or col == '7':
                                surf = graphics['objects'][int(col)]
                                Tree((x,y),[self.visible_sprites,self.obstacle_sprites, self.attackable_sprites], surf)
                        
                        elif style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack)
                                    # self.create_magic)
                            else:
                                if col == '390': monster_name   = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name              = 'squid'
                                Enemy(
                              		monster_name,
                              		(x,y),
                              		[self.visible_sprites,self.attackable_sprites],
                              		self.obstacle_sprites,
                              		self.damage_player,
                              		self.add_exp)

    def create_attack(self, attack_type):
        if attack_type == 'weapon':
            self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        else:
            self.current_attack = Fist(self.player, [self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'tree':
                            target_sprite.chop(self.player.get_full_weapon_damage(), self.current_attack)
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type = None):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
    
    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.display_surface, self.player)
        self.ui.display(self.player)
        if self.game_paused:
            self.upgrade_menu.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.clock.tick(FPS)
    
    def add_exp(self, amount):
        self.player.exp += amount

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()

        self.ground_surface = pygame.image.load('Zelda2D/assets/graphics/tilemap/ground.png')
        self.ground_rect = self.ground_surface.get_rect(topleft = (0, 0))
    
    def custom_draw(self, display_surface, player):
        self.offset.x  = player.rect.centerx - WIDTH//2
        self.offset.y  = player.rect.centery - HEIGHT//2

        self.ground_offset = self.ground_rect.topleft - self.offset
        display_surface.blit(self.ground_surface, self.ground_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)