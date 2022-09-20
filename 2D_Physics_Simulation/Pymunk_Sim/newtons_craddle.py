import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, draw_options, line):
    window.fill('white')
    if line:
        pygame.draw.line(window, 'black', line[0], line[1])
    space.debug_draw(draw_options)
    pygame.display.update()

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        shape.color = (20, 20, 20, 97)
        space.add(body, shape)

def create_pendulums(space, width, height):
    rad = 25

    rects = [
        [(width//2 - rad*4, 25), rad, 100],
        [(width//2 - rad*2, 25), rad, 100],
        [(width//2, 25), rad, 100],
        [(width//2 + rad*2, 25), rad, 100],
        [(width//2 + rad*4, 25), rad, 100]
    ]

    for pos, radius, mass in rects:
        rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        rotation_center_body.position = pos

        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = (pos[0], pos[1] + 200)

        circle = pymunk.Circle(body, radius)
        
        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))

        circle.friction = 0.01
        circle.mass = mass
        circle.elasticity = 1

        space.add(body, circle, rotation_center_joint)


def create_circle(space, radius, mass, pos):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = (pos)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.7
    shape.friction = 0.3
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    dt = 1/FPS

    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundaries(space, width, height)
    create_pendulums(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None

    while run:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_circle(space, 15, 10, pressed_pos)

                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line) # * asterisk breaks the list in the different elements
                    force = calculate_distance(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None

                else:
                    space.remove(ball, ball.body)
                    ball = None
                

        draw(space, window, draw_options, line)

        space.step(dt)
        clock.tick(FPS)

run(window, WIDTH, HEIGHT)
pygame.quit()