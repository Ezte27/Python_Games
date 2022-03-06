import pygame
from settings import *
import math, random

class Ball:
    def __init__(self, x, y, radius, color, max_vel = 5):
        self.original_x = x
        self.original_y = y
        self.x = self.original_x
        self.y = self.original_y
        self.radius = radius
        self.color = color
        self.angle = self.get_random_angle(-30, 30)
        self.x_vel = abs(math.cos(self.angle) * max_vel)
        self.y_vel = math.sin(self.angle) * max_vel
        self.max_vel = max_vel

    def get_random_angle(self, min_angle, max_angle):
        angle = math.radians(random.randrange(min_angle, max_angle))
        return angle

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        if (self.y - self.radius <= 0) or (self.y + self.radius >= HEIGHT):
            self.y_vel *= -1
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.angle = self.get_random_angle(-30, 30)
        self.x_vel = abs(math.cos(self.angle) * self.max_vel)
        self.y_vel = math.sin(self.angle) * self.max_vel