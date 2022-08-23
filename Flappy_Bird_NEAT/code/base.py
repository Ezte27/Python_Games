from tkinter import Y
import pygame
from settings import *

class Base:
    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = BASE_WIDTH
    
    def move(self):
        self.x1 -= BASE_VEL
        self.x2 -= BASE_VEL

        if self.x1 + BASE_WIDTH < 0:
            self.x1 = self.x2 + BASE_WIDTH
        
        if self.x2 + BASE_WIDTH < 0:
            self.x2 = self.x1 + BASE_WIDTH
    
    def draw(self, screen):
        screen.blit(BASE_IMG, (self.x1, self.y))
        screen.blit(BASE_IMG, (self.x2, self.y))