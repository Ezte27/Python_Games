from settings import HEIGHT

import pygame, math, random

class Ball:
    def __init__(self, pos, radius, color, max_vel):
        self.original_pos = pos
        self.x, self.y = pos[0], pos[1]
        self.x_vel = self.y_vel = 0
        self.radius = radius
        self.color = color
        self.max_vel = max_vel
    
    def move(self):
        # if (self.y - self.radius <= 0) or (self.y + self.radius >= HEIGHT):
        #     self.y_vel *= -1
        self.x += self.x_vel
        self.y += self.y_vel
        
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y, self.radius))
    
    def reset(self):
        self.x, self.y = self.original_pos[0], self.original_pos[1]
        self.x_vel = abs(math.cos(self.angle) * self.max_vel)
        self.y_vel = math.sin(self.angle) * self.max_vel
    
    def get_random_angle(self, min_angle, max_angle):
        angle = math.radians(random.randrange(min_angle, max_angle))
        return angle