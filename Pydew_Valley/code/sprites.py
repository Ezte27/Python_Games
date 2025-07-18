from settings import *
from timer import Timer
from random import randint, choice
import os
import pygame

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main'], name=None) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.35)
        self.name = name

class Interaction(Generic):
    def __init__(self, pos, size, groups, name) -> None:
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name

class WildFlower(Generic):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class HouseWall(Generic):
    def __init__(self, pos, surf, groups, name) -> None:
        super().__init__(pos, surf, groups, name=name)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.35)
        if name == "HouseWallsRight":
            self.hitbox.midleft = self.rect.midleft
        
        elif name == "HouseWallsLeft":
            self.hitbox.midright = self.rect.midright

class HouseRoof(Generic):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups, z=LAYERS["house roof"])
        self.hitbox = self.rect.copy()
        self.name = "HouseRoof"

class Water(Generic):
    def __init__(self, pos, frames, groups) -> None:
        
        # Animation Setup
        self.frames = frames
        self.frame_index = 0

        # Sprite Setup
        super().__init__(pos = pos,
                         surf=self.frames[self.frame_index],
                         groups=groups,
                         z = LAYERS['water'])
        
    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]
    
    def update(self, dt):
        self.animate(dt)

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200) -> None:
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # White Surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf
    
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add) -> None:
        super().__init__(pos, surf, groups)
        self.name = name

        # Tree Attributes
        self.health = TREE_MAX_HEALTH[self.name]
        self.daysToRegen = TREE_REVIVE_TIME # Count of days left to revive tree (if the tree has been cut down)
        self.isAlive = True
        self.tree_surf = surf
        self.stump_surf = pygame.image.load(os.path.join(PARENT_PATH, f"graphics/stumps/{name.lower()}.png")).convert_alpha()

        # Apples
        self.apples_surf = pygame.image.load(os.path.join(PARENT_PATH, "graphics/fruit/apple.png"))
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

        # Sounds
        self.axe_sound = pygame.mixer.Sound(os.path.join(PARENT_PATH, AXE_SOUND_PATH))
        self.axe_sound.set_volume(AXE_SOUND_VOLUME)

    def damage(self):
        # Damaging the tree
        self.health -= 1

        # Remove an apple
        if len(self.apple_sprites.sprites()):
            random_apple = choice(self.apple_sprites.sprites())
            Particle(
                pos = random_apple.rect.topleft,
                surf = random_apple.image,
                groups = self.groups()[0],
                z = LAYERS['fruit'], 
                duration=200
            )
            self.player_add('apple')
            random_apple.kill()
        
        # Play axe sound
        self.axe_sound.play()
    
    def check_death(self):
        if self.isAlive and self.health <= 0:
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS['fruit'], duration=400)
            self.player_add('wood', n = randint(1, 4) if self.name == 'Small' else randint(3, 8))
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            hitbox_midbottom = self.hitbox.midbottom # Take the full tree hitbox midbottom position
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height  * 0.6)
            self.hitbox.midbottom = hitbox_midbottom # Place the midbottom of the new hitbox in the midbottom of the full tree hitbox to avoid collision problems with the player
            self.isAlive = False

    def check_revive(self):
        if (self.daysToRegen <= 0) and (not self.isAlive) and (self.health <= 0):
            self.revive()
    
    def revive(self):
        # Surfaces and hitbox
        self.image = self.tree_surf
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        hitbox_midbottom = self.hitbox.midbottom # Take the full tree hitbox midbottom position
        self.hitbox = self.rect.copy().inflate(-10, -self.rect.height  * 0.3)
        self.hitbox.midbottom = hitbox_midbottom # Place the midbottom of the new hitbox in the midbottom of the full tree hitbox to avoid collision problems with the player
        
        # Create new fruit
        self.create_fruit()

        # Variables
        self.health = TREE_MAX_HEALTH[self.name]
        self.isAlive = True
        self.daysToRegen = TREE_REVIVE_TIME

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 3:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(pos = (x, y), surf = self.apples_surf, groups = [self.apple_sprites, self.groups()[0]], z = LAYERS['fruit'])
    
    def update(self, dt):
        self.check_death()
        # self.check_revive()
