import pygame
from settings import *
from perlin_noise import PerlinNoise

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_CAPTION)
clock = pygame.time.Clock()

# Create Height Map
# Use Perlin Noise to Generate the Terrain
def generate_terrain(octaves):
    noise = PerlinNoise(octaves=octaves)
    xpix, ypix = 200, 200

    height_map = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    return height_map


running = True
while running:
    clock.tick(FPS)

    # Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    


    pygame.display.update()

pygame.quit()