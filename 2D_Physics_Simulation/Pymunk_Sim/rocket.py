import pygame
import pymunk
import pymunk.pygame_util
import math
from random import randint, randrange, random
import numpy as np
from typing import Optional

# TODO
# - Try to make a new body named "MainEngine" and use a joint to connect it to the rocket; 
# In this way, you could apply a force and angle/gimbal to the engine and it would affect the entire rocket 

pygame.init()

# Display Setup

VIEWPORT_WIDTH         = 1920
VIEWPORT_HEIGHT        = 1020
WINDOW                 = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
CLOCK                  = pygame.time.Clock()

FPS                    = 60
SCALE                  = 1 # Temporal Scaling, lower is faster - adjust forces appropriately

# Pymunk Space Setup
X_GRAVITY, Y_GRAVITY   = (0, 956 * SCALE)
STARTING_POS           = (VIEWPORT_WIDTH//2, -200)

# Sky
SKY_COLOR              = (212, 234, 255)

MIN_THROTTLE           = 0.3
GIMBAL_THRESHOLD       = 0.2
MAIN_ENGINE_POWER      = 25000 * SCALE
SIDE_ENGINE_POWER      = 6000 * SCALE

# ROCKET
ROCKET_WIDTH           = 40 * SCALE
ROCKET_HEIGHT          = ROCKET_WIDTH * 5
ROCKET_SIZE            = (ROCKET_WIDTH, ROCKET_HEIGHT)
ROCKET_MASS            = 30 * SCALE
ROCKET_ELASTICITY      = 0.1
ROCKET_FRICTION        = 0.5
ROCKET_COLOR           = (161, 159, 159, 250)

# ENGINE
ENGINE_SIZE            = (ROCKET_WIDTH * 0.4, ROCKET_WIDTH * 0.5)
ENGINE_HEIGHT          = (ROCKET_HEIGHT/2) * 0.86
ENGINE_MASS            = ROCKET_MASS * 0.1
ENGINE_ELASTICITY      = 0.1
ENGINE_FRICTION        = 0.5
ENGINE_COLOR           = (111, 109, 109, 250)

# FIRE_WIDTH             = ROCKET_WIDTH * 3
# FIRE_HEIGHT            = FIRE_WIDTH * 3.4

# COLD_GAS_WIDTH         = FIRE_WIDTH/1.4
# COLD_GAS_HEIGHT        = COLD_GAS_WIDTH * 3

# CONTROL THRUSTERS
THRUSTER_HEIGHT        = (ROCKET_HEIGHT/2) * -0.86

# LEGS
LEG_HEIGHT             = ROCKET_SIZE[1] * 0.35
LEG_SPRING_HEIGHT      = ROCKET_SIZE[1] * 0.1
LEG_SIZE               = (ROCKET_SIZE[0] * 0.3, ROCKET_SIZE[1] * 0.4)
LEG_MASS               = 8 * SCALE
LEG_COLOR              = (220, 20, 30, 20)
LEG_ELASTICITY         = 0.3
LEG_FRICTION           = 0.6

# LEG_LENGTH             = ROCKET_WIDTH * 3
# LEG_WIDTH              = ROCKET_WIDTH * 0.8
# BASE_ANGLE             = -0.27
# SPRING_ANGLE           = 0.27
# LEG_AWAY               = ROCKET_WIDTH / 2

# WATER
WATER_HEIGHT           = 80 * SCALE
WATER_COLOR            = (0, 157, 196, 180)

# LANDING PAD
LANDING_PAD_HEIGHT     = ROCKET_WIDTH * 0.6
LANDING_PAD_WIDTH      = LANDING_PAD_HEIGHT * 18
LANDING_PAD_SIZE       = (LANDING_PAD_WIDTH, LANDING_PAD_HEIGHT)
LANDING_PAD_POS        = (VIEWPORT_WIDTH / 2, VIEWPORT_HEIGHT - (WATER_HEIGHT) - (LANDING_PAD_SIZE[1] / 2))

LANDING_PAD_ELASTICITY = 0.3
LANDING_PAD_FRICTION   = 0.7
LANDING_PAD_COLOR      = (50, 64, 63, 150)

# SMOKE FOR VISUALS
SMOKE_LIFETIME         = 0 # Lifetime
PARTICLE_TTL_SUBTRACT  = (1 / FPS)  # Amount to subtract ttl per frame
MAX_PARTICLES          = 100
PARTICLE_STARTING_TTL  = 1.0
SMOKE_RATE             = 0.98 # The rate at which the smoke gets generated. Range = [0 - PARTICLE_STARTING_TTL]
PARTICLE_GROWTH_RATE   = 20 / FPS
PARICLE_MAX_RADIUS     = 50 * SCALE
PARTICLE_Y_VEL_RANGE   = [100, 300]

# OTHER
DRAW_FLAGS             = False

class Rocket:

    metadata = {
        "render_modes": ["human", "rgb_array"], 
        "render_fps": FPS
    }

    def __init__(
        self, 
        space:       Optional[pymunk.Space] = None,
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
            self.clock   = pygame.time.Clock()
        else:
            self.clock   = None

        self.dt          = 1 / self.metadata['render_fps']
        self.render_mode = render_mode

        self.isopen      = True
        self.done        = False
        self.truncated   = False
        
        self._setup()

        self.throttle    = 0
        self.gimbal      = 0.0
        self.power       = 0
        self.force_dir   = 0

        self.engine_pos  = ()

        self.particles   = []

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
    
    def _setup(self,):

        self._create_water()
        
        self.lander, self.mainEngine = self._create_lander()

        self.legs                    = []
        self.leg_contacts            = []
        self._create_legs(self.lander.body)

        self.landing_pad             = self._create_landing_pad()
    
    def _create_lander(self):
        # Rocket
        size             = ROCKET_SIZE
        pos              = STARTING_POS

        inertia          = pymunk.moment_for_box(mass = ROCKET_MASS, size = ROCKET_SIZE)

        body             = pymunk.Body(mass = ROCKET_MASS, moment = inertia, body_type = pymunk.Body.DYNAMIC)
        body.position    = pos

        shape            = pymunk.Poly.create_box(body, size)
        shape.mass       = ROCKET_MASS
        shape.elasticity = ROCKET_ELASTICITY
        shape.friction   = ROCKET_FRICTION
        shape.color      = ROCKET_COLOR

        # Engine
        body_engine, shape_engine      = self._create_engine((body.position[0], body.position[1] + (ROCKET_SIZE[1] / 2) + ((ENGINE_SIZE[1] / 2) * 1.05)))

        # A PinJoint connecting the leg and the rocket
        pinjoint = pymunk.PinJoint(body_engine, body, (0, (-ENGINE_SIZE[1] / 2) * 1.05), (0, ROCKET_SIZE[1] / 2))
        pinjoint.max_force = 500000 * SCALE * 2

        self.space.add(body, shape, body_engine, shape_engine, pinjoint)

        return shape, shape_engine
    
    def _create_engine(self, pos):
        size             = ENGINE_SIZE

        inertia          = pymunk.moment_for_box(mass = ENGINE_MASS, size = size)

        body             = pymunk.Body(mass = ENGINE_MASS, moment = inertia, body_type = pymunk.Body.DYNAMIC)
        body.position    = pos

        shape            = pymunk.Poly.create_box(body, size)
        shape.mass       = ENGINE_MASS
        shape.elasticity = ENGINE_ELASTICITY
        shape.friction   = ENGINE_FRICTION
        shape.color      = ENGINE_COLOR

        return body, shape
    
    def _create_legs(self, rocket: pymunk.Body):

        leg_rects = [
            [LEG_SIZE, (rocket.position[0] - ROCKET_SIZE[0]//2 - LEG_SIZE[0]//2, rocket.position[1] + LEG_HEIGHT + LEG_SIZE[1]/2), -1],
            [LEG_SIZE, (rocket.position[0] + ROCKET_SIZE[0]//2 + LEG_SIZE[0]//2, rocket.position[1] + LEG_HEIGHT + LEG_SIZE[1]/2), 1]
        ]

        for size, pos, leg_side in leg_rects:
            inertia          = pymunk.moment_for_box(mass = LEG_MASS, size = size)

            body             = pymunk.Body(mass = LEG_MASS, moment = inertia, body_type = pymunk.Body.DYNAMIC)
            body.position    = pos

            shape            = pymunk.Poly.create_box(body, size)
            shape.mass       = LEG_MASS
            shape.elasticity = LEG_ELASTICITY
            shape.friction   = LEG_FRICTION
            shape.color      = LEG_COLOR

            # A PinJoint connecting the leg and the rocket
            pinjoint = pymunk.PinJoint(body, rocket, (-leg_side * LEG_SIZE[0]/2, -LEG_SIZE[1] / 2), (leg_side * ROCKET_SIZE[0]/2, LEG_HEIGHT))

            # A SlideJoint connecting the leg and the rocket
            slidejoint = pymunk.SlideJoint(body, rocket, (leg_side * LEG_SIZE[0]/2, LEG_SIZE[1] / 2.6), (leg_side * ROCKET_SIZE[0]/2, LEG_SPRING_HEIGHT), 100 * SCALE, 115 * SCALE)
            slidejoint.max_force = 50000 * SCALE * 2

            # A SpringJoint connecting the leg and the rocket
            springjoint = pymunk.DampedSpring(body, rocket, (leg_side * LEG_SIZE[0]/2, LEG_SIZE[1] / 2.6), (leg_side * ROCKET_SIZE[0]/2, LEG_SPRING_HEIGHT), -30000 * SCALE, -2.5, 10)
            springjoint.max_force = 8000 * SCALE * 2

            self.legs.append(shape)

            self.space.add(body, shape, pinjoint, slidejoint, springjoint)
        
        # A SpringJoint connecting both legs
        springjoint = pymunk.DampedSpring(self.legs[0].body, self.legs[1].body, (LEG_SIZE[0]/2, LEG_SIZE[1] / 3), (-LEG_SIZE[0]/2, LEG_SIZE[1] / 3), -1000 * SCALE, -2.5, 10)
        springjoint.max_force = 8000 * SCALE * 2
        self.space.add(springjoint)
    
    def _create_water(self):
        water_body          = pymunk.Body(body_type=pymunk.Body.STATIC)
        water_body.position = (VIEWPORT_WIDTH / 2, VIEWPORT_HEIGHT - (WATER_HEIGHT / 2))

        water               = pymunk.Poly.create_box(water_body, (VIEWPORT_WIDTH, WATER_HEIGHT))
        water.friction      = 3
        water.elasticity    = 0.2
        water.color         = WATER_COLOR
        self.space.add(water_body, water)

    def _create_landing_pad(self):
        size             = LANDING_PAD_SIZE
        pos              = LANDING_PAD_POS

        body             = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position    = pos
        shape            = pymunk.Poly.create_box(body, size)
        shape.elasticity = LANDING_PAD_ELASTICITY
        shape.friction   = LANDING_PAD_FRICTION
        shape.color      = LANDING_PAD_COLOR
        self.space.add(body, shape)

        return shape
    
    def _create_particle(self, mass, x, y, ttl, radius):
        color = (0, 0, 0, 0)

        p = [mass, (x, y), ttl, radius, color]

        self.particles.append(p)

    def _clean_particles(self, clean_all: bool):
        while self.particles and (clean_all or self.particles[0][2] <= 0):
            self.particles.pop(0)
    
    def _check_leg_contacts(self, check_landing_pad):
        contacts = []
        shape = self.landing_pad if check_landing_pad else self.water

        if len(self.legs) > 0 and ((self.landing_pad is not None and check_landing_pad is True) or (self.water is not None and check_landing_pad is not True)):
            for leg in self.legs:
                contacts.append((leg.shapes_collide(shape).normal)[1] >= 1)

        else:
            return [False, False]
        
        return contacts
    
    def _destroy(self):
        self.space = None

        self.lander = None
        self.water  = None
        self.landing_pad = None
        self.legs   = []
        self.leg_contacts = []

        self.screen  = None

        self.dt          = 0

        self.throttle   = 0
        self.gimbal     = 0.0
        self.power      = 0
        self.force_dir  = 0
        self.engine_pos = ()

        self.draw_options = None

        self._clean_particles(True)

    def reset(self, seed:int = None):
        self._destroy()
        
        self.space = pymunk.Space()

        self.space.gravity = (X_GRAVITY, Y_GRAVITY)

        self.screen  = pygame.display.get_surface()
        
        if self.clock:
            self.clock = pygame.time.Clock()
        else:
            self.clock = None

        self.dt          = 1 / self.metadata['render_fps']
        self.render_mode = self.render_mode

        self.isopen      = True
        self.done        = False
        
        self._setup()

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
        # Apply random angular vel to the rocket
        if seed:
            np.random.seed(seed)
        self.lander.body.apply_impulse_at_local_point((np.random.randint(-200 * SCALE, 200 * SCALE, 1), 0), (0, -ROCKET_SIZE[1]/2))

        return ...#observation, info
    
    def step(self, action):
        assert action != None

        self.force_dir = 0

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
        # force_pos = (self.lander.body.position[0] + (np.sin(-self.lander.body.angle) * ROCKET_HEIGHT/2), self.lander.body.position[1] + (np.cos(-self.lander.body.angle) * ROCKET_HEIGHT/2))
        # force = (-np.sin(-self.lander.body.angle + self.gimbal) * MAIN_ENGINE_POWER * self.power,
        #          np.cos(-self.lander.body.angle + self.gimbal) * MAIN_ENGINE_POWER * self.power)
        # force_pos = list(ENGINE_HEIGHT * np.array(
        #               (-np.sin(self.lander.body.angle), np.cos(self.lander.body.angle))))
        force_pos = (0, 0)
        force     = (0, -MAIN_ENGINE_POWER * self.power)

        #self.lander.body.apply_force_at_local_point(force = force, point = force_pos)
        self.mainEngine.body.apply_force_at_local_point(force = force, point = force_pos)

        self.debug = (self.lander.body.position[0] + force_pos[0], self.lander.body.position[1] + force_pos[1])

        # Main Engine Gimbal
        self.mainEngine.body.angle = self.lander.body.angle + self.gimbal
        
        # control thruster force
        force_pos_c = list(THRUSTER_HEIGHT * np.array(
                      (-np.sin(self.lander.body.angle), np.cos(self.lander.body.angle))))
        # force_c = (-self.force_dir * np.cos(self.lander.body.angle) * SIDE_ENGINE_POWER,
        #            self.force_dir * np.sin(self.lander.body.angle) * SIDE_ENGINE_POWER)
        force_c = (SIDE_ENGINE_POWER * self.force_dir, 0)
        #self.debug = (self.lander.body.position[0] + force_pos_c[0], self.lander.body.position[1] + force_pos_c[1])
        
        self.lander.body.apply_force_at_local_point(force = force_c, point=force_pos_c)

        self.engine_pos = (self.mainEngine.body.position[0] + (-np.sin(self.mainEngine.body.angle)), self.mainEngine.body.position[1] + (np.cos(self.mainEngine.body.angle)))

        # Checking for leg contact with landing pad
        self.leg_contacts = self._check_leg_contacts(True)

        self.space.step(self.dt)

        if self.render_mode == "human":
            self.render()

        return ...#observation, reward, done, truncated, info
    
    def render(self):

        self.surf = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
        self.particle_surf = self.surf.copy()

        pygame.draw.rect(self.surf, SKY_COLOR, self.surf.get_rect())
        pygame.draw.rect(self.particle_surf, (255, 255, 255), self.particle_surf.get_rect())

        for obj in self.particles:

            NewTTL = (((obj[2] - 0) * 2) / 1) - 1

            obj[1] = (obj[1][0], obj[1][1] + (randint(PARTICLE_Y_VEL_RANGE[0], PARTICLE_Y_VEL_RANGE[1]) / FPS) * NewTTL) # Move the smoke upwards
            obj[2] -= random() * PARTICLE_TTL_SUBTRACT # Take time from its lifetime
            obj[3] += PARTICLE_GROWTH_RATE if obj[3] < PARICLE_MAX_RADIUS else 0 # radius grows as the particle gets older
            ttl = 1 - obj[2]
            
            obj[4] = (
                int(ttl * 255),
                int(ttl * 255),
                int(ttl * 255),
                int(255)
            )

        # Drawing the Particles

        for obj in self.particles:
            try:
                pygame.draw.circle(
                    self.particle_surf,
                    color=obj[4],
                    center = (obj[1][0], obj[1][1]),
                    radius = obj[3], 
                )

            except ValueError: # particle RGB value is invalid
                ...

        # Draw Two Flags on either side of the landing pad

        if DRAW_FLAGS: 
            for i, x in enumerate([LANDING_PAD_POS[0] - LANDING_PAD_WIDTH/2, LANDING_PAD_POS[0] + LANDING_PAD_WIDTH/2]):
                flagy1 = LANDING_PAD_HEIGHT
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
                    # gfxdraw.aapolygon(
                    #     self.surf,
                    #     [(x, flagy2), (x, flagy2 - 10), (x - 25, flagy2 - 5)],
                    #     (204, 204, 0),
                    # )
                        
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
                    # gfxdraw.aapolygon(
                    #     self.surf,
                    #     [(x, flagy2), (x, flagy2 - 10), (x + 25, flagy2 - 5)],
                    #     (204, 204, 0),
                    # )

        # Create Smoke Particles
        if len(self.particles) <= MAX_PARTICLES:
            if self.particles:
                if self.particles[-1][2] < SMOKE_RATE * self.throttle:
                    self._create_particle(0.02, randrange(-10, 10) + self.engine_pos[0], randrange(-10, 10) + self.engine_pos[1], PARTICLE_STARTING_TTL, 8 * SCALE)
            else:
                if self.throttle > 0:
                    self._create_particle(0.02, randrange(-10, 10) + self.engine_pos[0], randrange(-10, 10) + self.engine_pos[1], PARTICLE_STARTING_TTL, 8 * SCALE)

        self._clean_particles(False)

        self.surf = pygame.transform.flip(self.surf, False, False)

        # DEBUG

        #surf = pygame.Surface(ROCKET_SIZE)
        #surf_trans = pygame.transform.rotate(surf, math.degrees(self.lander.body.angle))
        #rect = surf_trans.get_rect(center = self.lander.body.position)

        if self.render_mode == "human":
            assert self.screen is not None, "Screen is NONE"

            self.screen.blit(self.surf, (0, 0))

            self.screen.blit(self.particle_surf, (0, 0), special_flags= pygame.BLEND_RGBA_MULT)

            self.space.debug_draw(self.draw_options)

            pygame.draw.circle(self.screen, (255, 255, 255), self.debug, 10)

            pygame.event.pump()

            if self.clock is not None:
                self.clock.tick(self.metadata["render_fps"])

            pygame.display.flip()

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

    #create_boundaries(space, width, height)
    env = Rocket(render_mode = 'human', gravity = (X_GRAVITY, Y_GRAVITY))
    action = 0

    mouse_joint = None
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_joint is not None:
                    env.space.remove(mouse_joint)
                    mouse_joint = None

                p = pymunk.Vec2d(*event.pos)
                hit = env.space.point_query_nearest(p, 5, pymunk.ShapeFilter())
                if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                    shape = hit.shape
                    # Use the closest point on the surface if the click is outside
                    # of the shape.
                    if hit.distance > 0:
                        nearest = hit.point
                    else:
                        nearest = p
                    mouse_joint = pymunk.PivotJoint(
                        mouse_body, shape.body, (0, 0), shape.body.world_to_local(nearest)
                    )
                    mouse_joint.max_force = 80000
                    mouse_joint.error_bias = (1 - 0.15) ** 60
                    env.space.add(mouse_joint)

            elif event.type == pygame.MOUSEBUTTONUP:
                if mouse_joint is not None:
                    env.space.remove(mouse_joint)
                    mouse_joint = None

        keys = pygame.key.get_pressed()

        # Input
        if keys[pygame.K_LEFT]: # Increase Gimbal
            action =  0
        
        elif keys[pygame.K_RIGHT]: # Decrease Gimbal
            action =  1

        elif keys[pygame.K_w]: # Increase Throttle
            action =  2
        
        elif keys[pygame.K_s]: # Decrease Throttle
            action =  3
        
        elif keys[pygame.K_a]:
            action =  4
            #env.reset(seed = 19)
        
        elif keys[pygame.K_d]:
            action =  5
            #env.space.gravity = (0, 0)

        elif keys[pygame.K_LCTRL] and keys[pygame.K_s]: # Screenshot
            pygame.image.save(env.screen, "rocket_landing_sim_screenshot.png")
        
        elif keys[pygame.K_r]:
            env.reset()

        else:
            action = 6

        # Step
        env.step(action)

        # Mouse Interaction
        mouse_pos = pygame.mouse.get_pos()
        mouse_body.position = mouse_pos

        CLOCK.tick(FPS)

        pygame.display.set_caption(f"fps: {CLOCK.get_fps()}")

run()
pygame.quit()