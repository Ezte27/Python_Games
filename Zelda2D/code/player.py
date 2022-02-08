import pygame
from config import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load(r'C:\Users\ested\Documents\Programming\Python_Games\Zelda2D\assets\graphics\player\down_idle\idle_down.png').convert_alpha()
        self.rect  = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])
        
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.weapon_switch_cooldown = 300

        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        #stats
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 6
        }
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 0

        self.import_player_assets()

        self.obstacles = obstacles

    def import_player_assets(self):
        character_path = 'Zelda2D/assets/graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]
            }
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):
        if not self.attacking:
            keys_pressed = pygame.key.get_pressed()

            #Movement Input
            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
            
            if keys_pressed[pygame.K_q] and self.can_switch_weapon:
                if self.weapon_index >= 4:
                    self.weapon_index = -1 
                self.weapon_index += 1
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

            #Attack Input
            if keys_pressed[pygame.K_SPACE] and self.direction == (0, 0):
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            #Magic Input
            if keys_pressed[pygame.K_m]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('Magic')

    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    def animate_player(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_status(self):
        if self.direction == (0, 0):
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
            if self.attacking:
                self.direction.x = 0
                self.direction.y = 0
                if not 'attack' in self.status:
                    self.status = self.status.replace('idle', 'attack')
            else:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack', '')
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
                self.can_switch_weapon = True
    
    def update(self):
        self.input()
        self.cooldowns()
        self.move(self.speed)
        self.get_status()
        self.animate_player()