from random import randrange
import pygame
import pymunk
import pymunk.pygame_util
import math
import numpy as np
from typing import Optional

pygame.init()

# Display Setup

VIEWPORT_WIDTH         = 1000
VIEWPORT_HEIGHT        = 600
WINDOW                 = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))

FPS                    = 60
SCALE                  = 0.35  # Temporal Scaling, lower is faster - adjust forces appropriately

# Pymunk Space Setup

X_GRAVITY, Y_GRAVITY   = (0, int(956 * SCALE))
STARTING_POS           = (VIEWPORT_WIDTH//2, VIEWPORT_HEIGHT - 200)

# Sky
SKY_COLOR              = (126, 150, 233)

# ROCKET
MIN_THROTTLE           = 0.4
GIMBAL_THRESHOLD       = 0.4
MAIN_ENGINE_POWER      = 16000 * SCALE
SIDE_ENGINE_POWER      = 1200 / FPS * SCALE

ROCKET_WIDTH           = 6.5 * SCALE
ROCKET_HEIGHT          = ROCKET_WIDTH / 3.7 * 47.9
ENGINE_HEIGHT          = ROCKET_WIDTH * 0.5
ENGINE_WIDTH           = ENGINE_HEIGHT * 0.7

FIRE_WIDTH             = ROCKET_WIDTH * 3
FIRE_HEIGHT            = FIRE_WIDTH * 3.4

COLD_GAS_WIDTH         = FIRE_WIDTH/1.4
COLD_GAS_HEIGHT        = COLD_GAS_WIDTH * 3
THRUSTER_HEIGHT        = ROCKET_HEIGHT * 0.86

ROCKET_ELASTICITY      = 0.4
ROCKET_FRICTION        = 0.5
ROCKET_COLOR           = (20, 20, 20, 97)

# LEGS
LEG_LENGTH             = ROCKET_WIDTH * 2.2
BASE_ANGLE             = -0.27
SPRING_ANGLE           = 0.27
LEG_AWAY               = ROCKET_WIDTH / 2

# LANDING PAD
LANDING_PAD_HEIGHT     = ROCKET_WIDTH
LANDING_PAD_WIDTH      = LANDING_PAD_HEIGHT * 40

LANDING_PAD_ELASTICITY = 0.3
LANDING_PAD_FRICTION   = 0.6
LANDING_PAD_COLOR      = (220, 234, 233, 97)

# SMOKE FOR VISUALS
SMOKE_LIFETIME         = (FPS, 2 * FPS) # Smoke Lifetime ranges from 1*fps to 2*fps
MAX_PARTICLES          = 8

# OTHER
DRAW_FLAGS             = True

class Rocket:

    metadata = {
        "render_modes": ["human", "rgb_array"], 
        "render_fps": FPS
    }

    def __init__(
        self, 
        space:       Optional[pymunk.Space] = None,
        body:        Optional[pymunk.Body]  = None, 
        shape:       Optional[pymunk.Shape] = None,
        render_mode: Optional[str]          = None,
        gravity:     tuple                  = (0, 20),
        clock:       Optional[bool]         = False

    ) -> None:
        '''
        Create a Rocket object

        :py:data:`Hello World!`

        :Parameters:
                space : pymunk.Space
                    The basic unit of the pymunk simulation
        '''
        if space is None:
            self.space = pymunk.Space()

        else:
            self.space = space

        self.space.gravity = gravity

        self.screen  = pygame.display.get_surface()

        if render_mode not in self.metadata['render_modes']:
            raise Exception(f"The Render Mode provided is not available. \n Available Render Modes = {self.metadata['render_modes']}")

        if self.screen is None and render_mode == "human":
            self.screen = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
            print("[WARNING] pygame display NOT defined")
        
        if clock:
            self.clock = pygame.time.Clock()
        else:
            self.clock = None

        self.dt          = 1 / self.metadata['render_fps']
        self.render_mode = render_mode

        self.isopen      = True

        if body is not None and shape is not None:
            self.body, self.shape = body, shape
        
        else:
            self._setup()

        self.position  = pygame.math.Vector2((self.body.position))

        self.throttle  = 0
        self.gimbal    = 0.0
        self.power     = 0
        self.angle     = 0.0
        self.force_dir = 0

        self.particles = []

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
    
    def _setup(self,):
        size = (ROCKET_WIDTH, ROCKET_HEIGHT)
        pos =  STARTING_POS

        self.body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
        self.body.position = pos

        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = ROCKET_ELASTICITY
        self.shape.friction = ROCKET_FRICTION
        self.shape.color = ROCKET_COLOR
        self.space.add(self.body, self.shape)

        leg_rects = [
            [],
            []
        ]

        for leg in leg_rects:
            for pos, size in leg:
                pass
    
    def _create_particle(self, mass, x, y, ttl, radius):
        p = None
        # p = self.world.CreateDynamicBody(
        #     position=(x, y),
        #     angle=0.0,
        #     fixtures=fixtureDef(
        #         shape=circleShape(radius = radius, pos=(0, 0)),
        #         density=mass,
        #         friction=0.1,
        #         categoryBits=0x0100,
        #         maskBits=0x001,  # collide only with ground
        #         restitution=0.3,
        #     ),
        # )

        p.ttl = ttl
        self.particles.append(p)
        self._clean_particles(False)
        return p

    def _clean_particles(self, clean_all: bool):
        while self.particles and (clean_all or self.particles[0].ttl < 0):
            self.world.DestroyBody(self.particles.pop(0))
    
    def _create_landing_pad(self):
        rect = [
            (VIEWPORT_WIDTH / 2, VIEWPORT_HEIGHT - LANDING_PAD_HEIGHT),
            (LANDING_PAD_WIDTH, LANDING_PAD_HEIGHT)
        ]

        for pos, size in rect:
            body = pymunk.Body(body_type = pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = LANDING_PAD_ELASTICITY
            shape.friction   = LANDING_PAD_FRICTION
            shape.color      = LANDING_PAD_COLOR
            self.space.add(body, shape)
    
    def _destroy(self):
        if not self.water:
            return
        self.world.contactListener = None
        self.world.DestroyBody(self.water)
        self.water = None
        self.world.DestroyBody(self.lander)
        self.lander = None
        self.world.DestroyBody(self.ship)
        self.ship = None
        self.world.DestroyBody(self.legs[0])
        self.world.DestroyBody(self.legs[1])
        self.legs = []
        self.world.DestroyBody(self.containers[0])
        self.world.DestroyBody(self.containers[1])
        self.containers = []
        self.particles = []
        self.draw_options = None

    def reset(self):
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self._clean_particles(True)
    
    def step(self, action):

        if action == 0:    # Gimbal left
            self.gimbal += 0.01
        elif action == 1:  # Gimbal right
            self.gimbal -= 0.01
        elif action == 2:  # Increase Throttle
            self.throttle += 0.01
        elif action == 3:  # Decrease Throttle
            self.throttle -= 0.01
        elif action == 4:  # left control thruster
            self.force_dir = -1
        elif action == 5:  # right control thruster
            self.force_dir = 1
        else:              # No action
            ...

        self.gimbal = np.clip(self.gimbal, -GIMBAL_THRESHOLD, GIMBAL_THRESHOLD)
        self.throttle = np.clip(self.throttle, 0.0, 1.0)
        self.power = 0 if self.throttle == 0.0 else (MIN_THROTTLE + self.throttle * (1 - MIN_THROTTLE)) * (SCALE * 2)

        # main engine force
        force_pos = (self.position.x, self.position.y)
        force = (-np.sin(self.angle + self.gimbal) * MAIN_ENGINE_POWER * self.power,
                 np.cos(self.angle + self.gimbal) * MAIN_ENGINE_POWER * self.power)
        self.lander.ApplyForce(force=force, point=force_pos, wake=False)
        
        # control thruster force
        # force_pos_c = self.position + THRUSTER_HEIGHT * np.array(
        #               (np.sin(self.angle), np.cos(self.angle)))
        # force_c = (-self.force_dir * np.cos(self.angle) * SIDE_ENGINE_POWER,
        #            self.force_dir * np.sin(self.angle) * SIDE_ENGINE_POWER)

        self.space.step(self.dt)

        if self.render_mode == "human":
            self.render()

        return ...
    
    def render(self):

        self.surf = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))

        pygame.draw.rect(self.surf, SKY_COLOR, self.surf.get_rect())

        for obj in self.particles:
            obj.ttl -= 1 / randrange(SMOKE_LIFETIME)
            obj.color1 = (
                int(max(0.4, 0.6 * obj.ttl) * 255),
                int(max(0.4, 0.6 * obj.ttl) * 255),
                int(max(0.4, 0.6 * obj.ttl) * 255),
            )
            obj.color2 = (
                int(max(0.4, 0.6 * obj.ttl) * 255),
                int(max(0.4, 0.6 * obj.ttl) * 255),
                int(max(0.4, 0.6 * obj.ttl) * 255),
            )

        # Drawing the Particles and Pymunk Bodies
        '''
        for obj in self.particles + self.drawlist:
            for f in obj.fixtures:
                trans = f.body.transform
                if type(f.shape) is circleShape:
                    pygame.draw.circle(
                        self.surf,
                        color=obj.color1,
                        center=trans * f.shape.pos,
                        radius=f.shape.radius,
                    )
                    pygame.draw.circle(
                        self.surf,
                        color=obj.color2,
                        center=trans * f.shape.pos,
                        radius=f.shape.radius,
                    )

                else:
                    path = [trans * v for v in f.shape.vertices]
                    pygame.draw.polygon(self.surf, color=obj.color1, points=path)
                    gfxdraw.aapolygon(self.surf, path, obj.color1)
                    pygame.draw.aalines(
                        self.surf, color=obj.color1, points=path, closed=True
                    )

                if DRAW_FLAGS: # Draw Two Flags on either side of the helipad
    
                    for i, x in enumerate([self.helipad_x1, self.helipad_x2]):
                        flagy1 = self.helipad_y
                        flagy2 = flagy1 * 2
                        pygame.draw.line(
                            self.surf,
                            color=(255, 255, 255),
                            start_pos=(x, flagy1),
                            end_pos=(x, flagy2),
                            width=1,
                        )

                        if i == 0:
                            pygame.draw.polygon(
                                self.surf,
                                color=(204, 204, 0),
                                points=[
                                    (x, flagy2),
                                    (x, flagy2 - 10),
                                    (x - 25, flagy2 - 5),
                                ],
                            )
                            gfxdraw.aapolygon(
                                self.surf,
                                [(x, flagy2), (x, flagy2 - 10), (x - 25, flagy2 - 5)],
                                (204, 204, 0),
                            )
                        
                        else:
                            pygame.draw.polygon(
                                self.surf,
                                color=(204, 204, 0),
                                points=[
                                    (x, flagy2),
                                    (x, flagy2 - 10),
                                    (x + 25, flagy2 - 5),
                                ],
                            )
                            gfxdraw.aapolygon(
                                self.surf,
                                [(x, flagy2), (x, flagy2 - 10), (x + 25, flagy2 - 5)],
                                (204, 204, 0),
                            )
        '''

        if self.throttle > 0:
            
            # Create Smoke Particles
            if len(self.particles) <= MAX_PARTICLES:
                if self.particles:
                    if self.particles[-1].ttl < 0.6:
                        self._create_particle(0.02, randrange(-10, 10) + self.lander.position[0], randrange(-10, 10) + self.lander.position[1] - ENGINE_HEIGHT, 1.0, 45 * SCALE)
                else:
                    self._create_particle(0.02, randrange(-10, 10) + self.lander.position[0], randrange(-10, 10) + self.lander.position[1] - ENGINE_HEIGHT, 1.0, 45 * SCALE)

        self._clean_particles(False)

        self.surf = pygame.transform.flip(self.surf, False, True)

        if self.render_mode == "human":
            assert self.screen is not None, "Screen is NONE"

            self.space.debug_draw(self.draw_options)

            self.screen.blit(self.surf, (0, 0))

            pygame.event.pump()

            if self.clock is not None:
                self.clock.tick(self.metadata["render_fps"])

            pygame.display.update()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.surf)), axes=(1, 0, 2)
            )
    
    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()
            self.isopen = False

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

def run():
    
    window = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
    clock = pygame.time.Clock()
    FPS = 60

    #create_boundaries(space, width, height)
    rocket = Rocket(render_mode = 'human', gravity = (X_GRAVITY, Y_GRAVITY))
    action = 0

    # pressed_pos = None
    # ball = None

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Input
        if keys[pygame.K_w]:
            action =  2
        
        if keys[pygame.K_s]:
            action =  3
        
        if keys[pygame.K_a]:
            action =  0
        
        if keys[pygame.K_d]:
            action =  1

        # Step
        rocket.step(action)

        # line = None
        # if ball and pressed_pos:
        #     line = [pressed_pos, pygame.mouse.get_pos()]

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False

        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if not ball:
        #             pressed_pos = pygame.mouse.get_pos()
        #             ball = create_circle(space, 15, 10, pressed_pos)

        #         elif pressed_pos:
        #             ball.body.body_type = pymunk.Body.DYNAMIC
        #             angle = calculate_angle(*line) # * asterisk breaks the list in the different elements
        #             force = calculate_distance(*line) * 50
        #             fx = math.cos(angle) * force
        #             fy = math.sin(angle) * force
        #             ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
        #             pressed_pos = None

        #         else:
        #             space.remove(ball, ball.body)
        #             ball = None

        clock.tick(FPS)

run()
pygame.quit()