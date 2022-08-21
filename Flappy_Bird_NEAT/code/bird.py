import pygame
from settings import *

class Bird:
    def __init__(self, pos) -> None:
        
        # Bird attributes
        self.img = BIRD_IMGS[0]
        self.rect = self.img.get_rect(center = pos)

        # Animation
        self.img_count = 0

        # Movement
        self.x, self.y = pos
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count += 1
        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2

        if displacement >= 16:
            displacement = 16
        
        if displacement < 0:
            displacement -= 2
        
        self.y = self.y + displacement

        # Tilt Bird
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < MAX_ROTATION:
                self.tilt = MAX_ROTATION
        
        else:
            if self.tilt > -90:
                self.tilt -= ROT_VEL
    
    def draw(self, win):
        self.img_count += 1

        if self.img_count < ANIMATION_TIME:
            self.img = BIRD_IMGS[0]
        elif self.img_count < ANIMATION_TIME*2:
            self.img = BIRD_IMGS[1]
        elif self.img_count < ANIMATION_TIME*3:
            self.img = BIRD_IMGS[2]
        elif self.img_count < ANIMATION_TIME*4:
            self.img = BIRD_IMGS[1]
        elif self.img_count == ANIMATION_TIME*4 + 1:
            self.img = BIRD_IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = BIRD_IMGS[1]
            self.img_count = ANIMATION_TIME*2
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    