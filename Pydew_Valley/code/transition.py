import pygame
from settings import *

class Transition:
    def __init__(self, reset, player) -> None:
        
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = 300
        self.original_speed = self.speed

    def play(self, dt):
        self.color -= self.speed * dt
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            # Call Reset Day
            self.reset()
        if self.color >= 255:
            self.color = 255
            # Waking up player
            self.player.sleep = False
            
            # Speed changed to original value
            self.speed = self.original_speed
        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0,0), special_flags=pygame.BLEND_RGB_MULT) # pygame.BLEND_RGB_MULT for not showing white color