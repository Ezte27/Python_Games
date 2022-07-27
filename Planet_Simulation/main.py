import pygame
import math

pygame.init()

YELLOW = (240, 240, 40)
WHITE = (255, 240, 240)
BLACK = (0, 0, 0)
BLUE = (100, 120, 237)
RED = (230, 100, 102)
GRAY = (80, 78, 81)

WIDTH, HEIGHT = 800, 600
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

class Planet:
    AU = (149.6e6 * 1000)
    G = 6.67428e-11 
    SCALE = 250 / AU # 1AU = 100px
    TIMESTEP = 3600 * 24 # one day in seconds

    def __init__(self, x, y, radius, color, mass) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        pygame.draw.circle(window, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x

def main(FPS):
    running = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)

    mercury = Planet(0.387 * Planet.AU, 0, 8, GRAY, 3.30 * 10**23)

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**2)

    planets = [sun, mercury, venus, earth, mars]

    while running:
        clock.tick(FPS)
        window.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
            
        for planet in planets:
            planet.draw(window)
        
        pygame.display.update()

    pygame.quit()

main(FPS)