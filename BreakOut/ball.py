from settings import WIDTH, MIN_ANGLE, MAX_ANGLE

import pygame, math, random

class Ball:
    def __init__(self, pos, radius, color, max_vel):
        self.original_pos = pos
        self.x, self.y = pos[0], pos[1]
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.max_vel = max_vel
        self.angle = self.get_random_angle(MIN_ANGLE, MAX_ANGLE)
        self.x_vel = self.angle[0] * self.max_vel
        self.y_vel = self.angle[1] * self.max_vel
    
    def move(self):
        if (self.x - self.radius <= 0) or (self.x + self.radius >= WIDTH):
            self.x_vel *= -1
        self.x += self.x_vel
        self.y += self.y_vel
    
    def draw(self, win):
        self.rect = pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def reset(self):
        self.x, self.y = self.original_pos[0], self.original_pos[1]
        self.angle = self.get_random_angle(MIN_ANGLE, MAX_ANGLE)
        self.x_vel = self.angle[0] * self.max_vel
        self.y_vel = self.angle[1] * self.max_vel
        self.rect.x, self.rect.y = self.x, self.y
    
    def get_random_angle(self, min_angle: float, max_angle: float):
        angle = [0, 0]
        angle[0] = random.randint(min_angle[0], max_angle[0])
        angle[1] = min_angle[1]
        return angle