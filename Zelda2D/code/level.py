import pygame
from weapon import Weapon
from config import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder
from random import choice
from ui import UI
from tree import Tree

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

        self.ui = UI()

        self.create_map()
    
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
                        #print(col)
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
                                [self.visible_sprites,self.obstacle_sprites],
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
                                pass
                            # else:
                            # 	if col == '390': monster_name = 'bamboo'
                            # 	elif col == '391': monster_name = 'spirit'
                            # 	elif col == '392': monster_name ='raccoon'
                            # 	else: monster_name = 'squid'
                            # 	Enemy(
                            # 		monster_name,
                            # 		(x,y),
                            # 		[self.visible_sprites,self.attackable_sprites],
                            # 		self.obstacle_sprites,
                            # 		self.damage_player,
                            # 		self.trigger_death_particles,
                            # 		self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None
    
    def check_tree_attack(self):
        if self.current_attack:
            for tree in self.attackable_sprites.sprites():
                if self.current_attack.rect.colliderect(tree.rect) and tree.current_attack != self.current_attack:
                    tree.health -= 1
                    tree.current_attack = self.current_attack
                    if tree.health <= 0:
                        tree.kill()
                        self.player.health += 5
                        self.player.health = 100 if self.player.health >= 100 else self.player.health

    def run(self):
        self.visible_sprites.custom_draw(self.display_surface, self.player)
        self.visible_sprites.update()
        self.check_tree_attack()
        self.ui.display(self.player)
        self.clock.tick(FPS)

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