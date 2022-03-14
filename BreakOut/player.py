import pygame

class Player:
    def __init__(self, pos, width, height, color, speed):
        self.original_pos = pos
        self.x, self.y = pos[0], pos[1]
        self.width = width
        self.height = height
        self.color = color
        self.SPEED = speed
    
    def move(self, right = None):
        if right:
            self.x += self.SPEED
        elif not right:
            self.x -= self.SPEED
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    
    def reset(self):
        self.x, self.y = self.original_pos[0], self.original_pos[1]