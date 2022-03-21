import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()
WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, draw_options):
    window.fill('white')
    space.debug_draw(draw_options)
    pygame.display.update()

def create_circle(space, radius, mass):
    body = pymunk.Body()
    body.position = (WIDTH/2, HEIGHT/2)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    ball = create_circle(space, 30, 10)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        draw(space, window, draw_options)

        space.step(dt)
        clock.tick(fps)

if __name__ == '__main__':
    run(window, WIDTH, HEIGHT)