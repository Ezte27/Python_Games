import pygame, math
from random import randint, choice

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CAPTION = "Particle Sim"
FPS = 30

BLACK = (0, 0, 0)

PARTICLE_RADIUS = 5
PARTICLE_RANGE = PARTICLE_RADIUS * 40
PARTICLE_MASS = 0.01 # kg

PARTICLE_QUANTITY = 3

SPEED = 2000000000000000000

color_attributes_attract = { # Move towards
    'red': ['green'],
    'green': ['blue'],
    'blue': ['red']
}

color_attributes_repel = { # Move away
    'red': ['green'], # It was blue
    'green': ['red'],
    'blue': ['green']
}

COLORS = ['red', 'green', 'blue'] # All available colors

G = 6.674 * (10**-11) # Gravitational constant

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(SCREEN_CAPTION)

class Particle:
    def __init__(self, color, range, mass, pos=()) -> None:
        self.w = PARTICLE_RADIUS*1.5
        self.h = PARTICLE_RADIUS*1.5
        self.color = color
        self.mass = mass
        
        self.rect = self.random_rect()
        if pos:
            self.rect.center = pos
        self.range = range # Range should be a radius not total length
        self.range_circle = pygame.Rect(self.rect.x, self.rect.y, self.w + self.range*2, self.h + self.range*2)
        self.vel_x = 0
        self.vel_y = 0
        self.direction = pygame.math.Vector2((1,1))
    
    def random_rect(self):
        return pygame.Rect(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT), self.w, self.h)

    def find_particles_in_range(self, particles):
        particles_in_range = []
        for particle in particles:
            particles_in_range.append(particle) if self.range_circle.colliderect(particle.rect) else None
        return particles_in_range
    
    # def interact(self, particles_in_range):
    #     for particle in particles_in_range:
    #         if self.rect.collidepoint(particle.rect.left) or self.rect.collidepoint(particle.rect.right): # horizontal collision
    #             particle.vel_x *= -1
    #         if self.rect.collidepoint(particle.rect.top) or self.rect.collidepoint(particle.rect.bottom): # vertical collision
    #             particle.vel_y *= -1

    def attract_or_repel(self, color):
        a = True if color in color_attributes_attract[self.color] else False
        r = True if color in color_attributes_repel[self.color] else False
        return (a, r)
    
    def repel(self, particle):
        d = math.sqrt(((self.rect.x - particle.rect.x)**2) + ((self.rect.y - particle.rect.y)**2))
        force = ((self.mass * particle.mass)/(d**2)) * G
        force_angle = math.atan((particle.rect.x - self.rect.x)/(particle.rect.y - self.rect.y))
        force_x = force/(math.cos(force_angle))
        force_y = force/(math.sin(force_angle))
        self.vel_x -= force_x * SPEED
        self.vel_y -= force_y * SPEED

    def attract(self, particle):
        d_x = (particle.rect.x - self.rect.x)
        d_x = 0.000000000000001 if d_x == 0 else d_x
        d_y = (particle.rect.y - self.rect.y)
        d_y = 0.000000000000001 if d_y == 0 else d_y
        d = math.sqrt(((d_x)**2) + ((d_y)**2))
        d =   0.000000000000001 if d == 0 else d
        force = ((self.mass * particle.mass)/(d**2)) * G
        force_angle = math.atan((d_x)/(d_y))
        force_x = force/(math.cos(force_angle))
        force_y = force/(math.sin(force_angle))
        self.vel_x += force_x * SPEED
        self.vel_y += force_y * SPEED
        self.direction.x = 1 if (d_x) >= 0 else -1
        self.direction.y = 1 if (d_y) >= 0 else -1

    def move(self, dt, particles):
        particles_in_range = self.find_particles_in_range(particles)
        # self.interact(particles_in_range)
        for particle in particles_in_range:
            if self.attract_or_repel(particle.color)[0]:
                self.attract(particle)
            elif self.attract_or_repel(particle.color)[1]:
                self.repel(particle)
            else:
                continue

        self.rect.x += self.direction.x * self.vel_x * dt
        self.rect.y += self.direction.y * self.vel_y * dt
        self.range_circle.center = self.rect.center
        # if self.color == 'blue':
        #     print(self.vel_x, self.vel_y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, PARTICLE_RADIUS)
        pygame.draw.circle(screen, 'white', self.range_circle.center, PARTICLE_RANGE, width=4)
    
    def update(self, dt, particles, screen):
        self.move(dt, particles)
        self.draw(screen)

particles = [Particle('blue', PARTICLE_RANGE, PARTICLE_MASS, pos=(300, 300)), Particle('red', PARTICLE_RANGE, PARTICLE_MASS, pos=(280, 280))]#[Particle(choice(COLORS), PARTICLE_RANGE, PARTICLE_MASS) for i in range(0, PARTICLE_QUANTITY)]

dt = 0.001
running = True
while running:
    clock.tick(FPS)

    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for particle in particles:
        particle.update(dt, particles, screen)

    pygame.display.update()

pygame.quit()