from random import randint
import pygame
import os
from support import import_folder
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction
from transition import Transition
from soil import SoilLayer
from sky import Rain
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self) -> None:

        # get current display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite Groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # Extra
        self.cwd = os.getcwd()

        # Soil
        self.soil_layer = SoilLayer(self.all_sprites)

        # Sky
        self.rain = Rain(self.all_sprites)
        self.raining = False
        self.soil_layer.raining = self.raining

        # Setup
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset_day, self.player)

    def setup(self):
        tmx_data = load_pygame(f"{self.cwd}/data/map.tmx")

        # House
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])
        
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites], LAYERS['main'])

        # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['main'])

        # Water
        water_frames = import_folder(f"{self.cwd}/graphics/water")
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # WildFlower
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])
        
        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name, player_add = self.player_add_item)

        # Ground
        Generic((0, 0), pygame.image.load(os.getcwd() + '/graphics/world/ground.png').convert_alpha(), self.all_sprites, z=LAYERS['ground'])
        
        # Collision Tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), [self.collision_sprites])

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), [self.all_sprites], self.collision_sprites, self.tree_sprites, interaction = self.interaction_sprites, soil_layer = self.soil_layer)
            if obj.name == "Bed":
                Interaction((obj.x, obj.y), (obj.width, obj.height), [self.interaction_sprites], obj.name)
    
    def player_add_item(self, item, n = 1):
        self.player.item_inventory[item] += n
    
    def reset_day(self):

        # Trees
        for tree in self.tree_sprites.sprites():
            if tree.isAlive:
                for apple in tree.apple_sprites.sprites():
                    apple.kill()
                tree.create_fruit()

        # Soil
        self.soil_layer.remove_water()

        # Raining
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player) # The draw function from pygame.sprite.Group()
        self.all_sprites.update(dt)

        # Rain
        if self.raining:
            self.rain.update()

        self.overlay.display()

        # Transition Overlay
        if self.player.sleep:
            self.transition.play(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    
    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # if sprite == player:
                    #     pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                    #     hitbox_rect = player.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect,5)