from random import randint, choice
import pygame
from settings import *
from support import import_folder
from sprites import Generic
from timer import Timer

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

class Sky:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.start_color = [255, 255, 255]
        self.end_color = (20, 25, 60)

        self.color_index = [0, 0, 0]

        self.sunrise = False
        self.sunset = True

        # Timers
        self.timer = Timer((1/DAYTIME_SPEED) * DAY_NIGHT_DURATION)

    def display(self, dt):
        self.timer.update()

        if not self.timer.active:
            if self.sunset:
                for index, value in enumerate(self.end_color):
                    if self.start_color[index] > value:
                        self.start_color[index] -= DAYTIME_SPEED * dt
                    else:
                        self.color_index[index] = 1
                    
                if all(self.color_index):
                    self.sunrise = True
                    self.sunset  = False
                    self.timer.activate()
                    print("timer")
            
            elif self.sunrise:
                for index, value in enumerate(self.end_color):
                    if self.start_color[index] < 255:
                        self.start_color[index] += DAYTIME_SPEED * dt
                    else:
                        self.color_index[index] = 0

                if not(all(self.color_index)):
                    self.sunrise = False
                    self.sunset  = True
                    self.timer.activate()

        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0,0), special_flags= pygame.BLEND_RGBA_MULT) # dont show white FLAG