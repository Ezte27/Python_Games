from random import randint, choice
import pygame
from settings import *
from support import import_folder
from sprites import Generic

class Rain:
    def __init__(self, all_sprites) -> None:
        self.display_surface = pygame.display.get_surface()
        
        self.all_sprites = all_sprites
        self.rain_drops = import_folder("graphics/rain/drops/")
        self.rain_floor = import_folder("graphics/rain/floor/")
        self.floor_w, self.floor_h = pygame.image.load("graphics/world/ground.png").get_size()
        
        # Fog
        self.fog_color = randint(140,180)

    def create_floor(self):
        Drop((randint(0, self.floor_w), randint(0, self.floor_h)), choice(self.rain_floor), moving=False, groups = [self.all_sprites], z=LAYERS['rain floor'])

    def create_drops(self):
        Drop((randint(0, self.floor_w), randint(0, self.floor_h)), choice(self.rain_drops), moving=False, groups = [self.all_sprites], z=LAYERS['rain drops'])

    def create_fog(self):
        self.fog_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fog_img.fill((self.fog_color, self.fog_color, self.fog_color))
        self.display_surface.blit(self.fog_img, (0,0), special_flags=pygame.BLEND_RGB_MULT) # pygame.BLEND_RGB_MULT for not showing white color

    def randomize_fog(self):
        self.fog_color = randint(140,180)

    def update(self):
        self.create_floor()
        self.create_drops()
        self.create_fog()

class Drop(Generic):
    def __init__(self, pos, surf, moving, groups, z) -> None:
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400,500)
        self.start_time = pygame.time.get_ticks()

        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(300, 500)
    
    def update(self, dt):
        # Movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # Timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()