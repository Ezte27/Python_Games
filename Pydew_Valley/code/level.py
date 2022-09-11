from random import randint
import pygame
import os
from support import import_folder
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle, HouseWall, HouseRoof
from entities import Entity
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from menu import Menu
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
        self.houseRoof_sprites = pygame.sprite.Group()

        # Extra
        self.cwd = os.getcwd()

        # Soil
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        # Sky
        self.rain = Rain(self.all_sprites)
        self.sky = Sky()
        self.raining = False
        self.soil_layer.raining = self.raining

        # Setup
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset_day, self.player, self.houseRoof_sprites)

        # Shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        # Sounds
        self.success_sound = pygame.mixer.Sound(f"{os.getcwd()}{SUCCESS_SOUND_PATH}")
        self.success_sound.set_volume(SUCCESS_SOUND_VOLUME)

        self.bg_music = pygame.mixer.Sound(f"{os.getcwd()}{BG_MUSIC_SOUND_PATH}")
        self.bg_music.set_volume(BG_MUSIC_SOUND_VOLUME)

        # Background Music
        self.bg_music.play(loops = -1)

    def setup(self):
        tmx_data = load_pygame(f"{self.cwd}/data/map.tmx")

        # House
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])
        
        for layer in ["HouseWalls", "HouseFurnitureTop"]: # Put "HouseWalls first or else for some reason, half of the bed will no be seen" (maybe because they have the same y position)
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites], LAYERS['main'])
        
        for x, y, surf in tmx_data.get_layer_by_name('HouseWallsLeft').tiles():
            HouseWall((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], name = 'HouseWallsLeft')

        for x, y, surf in tmx_data.get_layer_by_name('HouseWallsRight').tiles():
            HouseWall((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], name = 'HouseWallsRight')
        
        for x, y, surf in tmx_data.get_layer_by_name('HouseRoof').tiles():
            HouseRoof((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.houseRoof_sprites])

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
                self.player = Player((obj.x, obj.y), [self.all_sprites], self.collision_sprites, self.tree_sprites, interaction = self.interaction_sprites, soil_layer = self.soil_layer, toggle_shop = self.toggle_shop)
            elif obj.name == "Bed":
                Interaction((obj.x, obj.y), (obj.width, obj.height), [self.interaction_sprites], obj.name)
            elif obj.name == "Trader":
                Interaction((obj.x, obj.y), (obj.width, obj.height), [self.interaction_sprites], obj.name)
        
        # Entities
        # Entity((900, 900), pygame.image.load(f"{os.getcwd()}/graphics/mobs/pig/Pig1.png").convert_alpha(), [self.all_sprites])
    
    def player_add_item(self, item, n = 1):

        self.player.inventory[item] += n
        self.success_sound.play()
    
    def toggle_shop(self):

        # Toggle the shop
        self.shop_active = not self.shop_active

        # Activate Timer when opening the shop to ignore input for some time
        self.menu.move_timer.activate() if (not self.menu.move_timer.active) and (self.shop_active) else None
    
    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add_item(plant.plant_type)
                    plant.kill()
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, LAYERS['main'])
                    x = plant.rect.midbottom[0] // TILE_SIZE
                    y = plant.rect.midbottom[1] // TILE_SIZE
                    self.soil_layer.grid[y][x].remove('P')
    
    def reset_day(self):

        # Trees
        for tree in self.tree_sprites.sprites():
            if tree.isAlive:
                for apple in tree.apple_sprites.sprites():
                    apple.kill()
                tree.create_fruit()

        # Raining
        self.raining = randint(0, 10) <= RAIN_PROBABILITY
        self.soil_layer.raining = self.raining
        
        # Plants
        self.soil_layer.update_plants()

        # Soil (first check for watered soil in update_plants() before removing the water)
        self.soil_layer.remove_water()

        # Sky
        self.sky.reset()
    
    def check_house_roof_visibility(self) -> bool:
        '''Return True if player collides with house roof'''
        for sprite in self.houseRoof_sprites.sprites():
            if self.player.hitbox.colliderect(sprite.hitbox):
                return True
        return False

    def run(self, dt):

        # Drawing Logic
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player) # The draw function from pygame.sprite.Group()
        
        # Updates
        if self.shop_active:
            self.menu.update()

        if not self.shop_active:
            self.all_sprites.update(dt)
            self.plant_collision()

            # Rain
            if self.raining:
                self.rain.update()
                self.soil_layer.water_all() # Water all soil plots

        # Daytime
        self.sky.display(dt)

        self.overlay.display()

        # House Roof
        if self.check_house_roof_visibility():
            self.transition.play_house_roof(dt, 1)
        else:
            self.transition.play_house_roof(dt, 0)

        # if self.check_house_roof_visibility():
        #     for sprite in self.all_sprites.sprites():
        #         if hasattr(sprite, 'name') and sprite.name == "HouseRoof":
        #             self.all_sprites.remove(sprite)
            
        # else:
        #     self.all_sprites.add(self.houseRoof_sprites.sprites())

        # Transition Overlay
        if self.player.sleep:
            self.transition.play_sleep(dt)

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

                    # DEBUG
                    # if sprite == player:
                    #     hitbox_rect = player.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect,3)

                    # if hasattr(sprite, "name") and sprite.name == "Small":
                    #     hitbox = sprite.hitbox.copy()
                    #     hitbox.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface, "Red", hitbox, 3)