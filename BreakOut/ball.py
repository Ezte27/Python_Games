from settings import WIDTH, MIN_ANGLE, MAX_ANGLE

import pygame, math, random

class Ball:
    def __init__(self, pos, radius, color, max_vel):
        self.original_pos = pos
        self.x, self.y = pos[0], pos[1]
        self.radius = radius
        self.color = color
        self.max_vel = max_vel
        self.angle = self.get_random_angle(MIN_ANGLE, MAX_ANGLE)
        self.x_vel = abs(math.cos(self.angle) * self.max_vel)
        self.y_vel = math.sin(self.angle) * self.max_vel
    
    def move(self):
        if (self.x - self.radius <= 0) or (self.x + self.radius >= WIDTH):
            self.x_vel *= -1
        self.x += self.x_vel
        self.y += self.y_vel
        
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def reset(self):
        self.x, self.y = self.original_pos[0], self.original_pos[1]
        self.x_vel = abs(math.cos(self.angle) * self.max_vel)
        self.y_vel = math.sin(self.angle) * self.max_vel
    
    def get_random_angle(self, min_angle: int, max_angle: int):
        angle = math.radians(random.choice([min_angle, max_angle]))
        return angle