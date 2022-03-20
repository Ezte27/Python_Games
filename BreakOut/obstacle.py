import pygame

class Obstacle:
    def __init__(self, pos, width, height, color):
        self.x, self.y = pos[0], pos[1]
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)