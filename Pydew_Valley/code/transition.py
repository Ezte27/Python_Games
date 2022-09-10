import pygame
from settings import *

class Transition:
    def __init__(self, reset, player, roof_sprites:pygame.sprite.Group) -> None:
        
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player
        self.roof_sprites = roof_sprites

        # overlay images for sleep
        self.sleep_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.sleep_color = 255
        self.sleep_speed = 300
        self.sleep_original_speed = self.sleep_speed

        # Setup for roofs
        self.roof_speed = 300
        self.alpha      = 255

    def play_house_roof(self, dt, direction:int):
        """ direction between 0 and 1, direction of 0 is motion out of the house while direction of 1 is motion into the house""" # if direction == 0 then the roof's alpha value is going up if direction == 1 then the roof's alpha value is going down
        if not(any([(direction == 0), direction == 1])):
            raise ValueError("Direction argument must be 0 or 1")
        
        if direction and self.alpha != 0: # Alpha transition from 255 to 0
            self.alpha -= self.roof_speed * dt
            for sprite in self.roof_sprites.sprites():
                sprite.image.set_alpha(self.alpha) 
                if self.alpha <= 0:
                    self.alpha = 0
        elif not(direction) and self.alpha != 255: # Alpha transition from 0 to 255
            self.alpha += self.roof_speed * dt
            for sprite in self.roof_sprites.sprites():
                sprite.image.set_alpha(self.alpha) 
                if self.alpha >= 255:
                    self.alpha = 255 
    
    def play_sleep(self, dt):
        self.sleep_color -= self.sleep_speed * dt
        if self.sleep_color <= 0:
            self.sleep_speed *= -1
            self.sleep_color = 0
            # Call Reset Day
            self.reset()
        if self.sleep_color >= 255:
            self.sleep_color = 255
            # Waking up player
            self.player.sleep = False
            
            # Speed changed to original value
            self.sleep_speed = self.sleep_original_speed
        self.sleep_image.fill((self.sleep_color, self.sleep_color, self.sleep_color))
        self.display_surface.blit(self.sleep_image, (0,0), special_flags=pygame.BLEND_RGB_MULT) # pygame.BLEND_RGB_MULT for not showing white color