import pygame
from settings import *
from random import randrange

class Pipe:
    def __init__(self, x) -> None:
        self.x = x
        self.height = 0
        self.gap = 100
        
        self.top = 0
        self.bottom = 0
        
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = randrange(100, 300)
        self.top = self.height - PIPE_TOP.get_height()
        self.bottom = self.height + GAP
    
    def move(self):
        self.x -= PIPE_VEL
    
    def draw(self, win):
        win.blit(PIPE_TOP, (self.x, self.top))
        win.blit(PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False