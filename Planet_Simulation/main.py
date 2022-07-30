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

FONT = pygame.font.SysFont("comicsans", 16)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")


class Planet:
    AU = (149597870.7)  # 149600000000.0 km 149598000
    G = 6.67428e-11
    SCALE = 100.0/AU  # 100 / AU # 1AU = 100px /// 0.00006147717 = 150 / AU
    TIMESTEP = 3600 * 24 / 200000  # one day in seconds

    def __init__(self, x, y, radius, color, mass) -> None:
        self.x = x
        self.y = y
        self.original_radius = radius
        self.radius = self.original_radius * self.SCALE
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

        self.rect = pygame.Rect(self.x, self.y, math.sqrt(
            2) * self.radius, math.sqrt(2) * self.radius)

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        self.rect.x = x
        self.rect.y = y

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x_point, y_point = point
                x_point = x_point * self.SCALE + WIDTH / 2
                y_point = y_point * self.SCALE + HEIGHT / 2
                updated_points.append((x_point, y_point))

            pygame.draw.lines(window, self.color, False, updated_points)
        self.radius = self.original_radius * self.SCALE
        pygame.draw.circle(window, self.color, (x, y), self.radius)
        if self.mass == 5.972 * 10**24:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun, 1)}km", 1, WHITE)
            window.blit(distance_text, (x - distance_text.get_width() /
                        2, y - distance_text.get_height()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def check_collision(self, planets: list):
        for planet in planets:
            if planet == self:
                continue

            if self.rect.colliderect(planet.rect) and not planet.sun:
                return (planet)
        return False
    
    def erase_old_orbit(self):
        pass


def main(FPS):
    running = True
    clock = pygame.time.Clock()

    # Sun radius = 0.4654 if SCALE = 100px/AU
    sun = Planet(0, 0, 30000000, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    # xAU, yAU, radius in px, color, mass in kilograms
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.972 * 10**24)
    earth.y_vel = 29.8 * 31700  # Kilometers per second

    # moon = Planet(-0.99 * Planet.AU, 0, 2.5, GRAY, 7.34767309 * 10**22)
    # moon.y_vel = 29.783 * 1000

    mars = Planet(-1.39915093056 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.37558689664 * Planet.AU, 0, 8, GRAY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.721066412879 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**2)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth]

    while running:
        clock.tick(FPS)
        window.fill(BLACK)
        # print(earth.x * earth.SCALE + WIDTH/2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # Scroll behavior
                if event.button == 4:  # Up scroll
                    for planet in planets:
                        planet.SCALE += 0.0000001

                elif event.button == 5:  # Down scroll
                    for planet in planets:
                        if planet.SCALE > 0.0000005:
                            planet.SCALE -= 0.0000001

                        else:
                            planet.SCALE = 0.0000005
                        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            for planet in planets:
                planet.y += 4000000000000 * planet.SCALE

        if keys[pygame.K_DOWN]:
            for planet in planets:
                planet.y -= 4000000000000 * planet.SCALE

        if keys[pygame.K_RIGHT]:
            for planet in planets:
                planet.x -= 4000000000000 * planet.SCALE

        if keys[pygame.K_LEFT]:
            for planet in planets:
                planet.x += 4000000000000 * planet.SCALE

        for planet in planets:
            collision = planet.check_collision(planets)
            if collision:
                planets.remove(collision)

            if not planet.sun:
                # The sun does not move in this current version of the simulation.
                planet.update_position(planets)
            planet.draw(window)

        debug_text = FONT.render(f"{sun.y} sun y", False, WHITE)
        window.blit(debug_text, (10, 10))

        pygame.display.update()

    pygame.quit()


main(FPS)
