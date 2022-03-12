import pygame
from settings import *

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.original_x = x
        self.original_y = y
        self.x = self.original_x
        self.y = self.original_y
        self.width = width
        self.height = height
        self.color = color
        self.SPEED = 4
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True):
        if up:
            self.y -= self.SPEED
        elif not up:
            self.y += self.SPEED
        else:
            pass
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y