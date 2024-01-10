from config import *
from support import *
from entity import Entity
import os
import pygame

class Enemy(Entity):
    def __init__(self,monster_name,  pos, groups, obstacles, damage_player, add_exp):
        super().__init__(groups)
        
        self.sprite_type = 'enemy'
        self.monster_name = monster_name

        #graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-120 if self.monster_name == 'raccoon' else 0, HITBOX_OFFSET[self.monster_name])
        self.obstacles = obstacles

        # stats
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        
        self.can_attack = True
        self.attack_time = None
        self.cooldown = 400
        self.damage_player = damage_player
        self.add_exp = add_exp

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
    
    def import_graphics(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        full_path = os.path.join(PARENT_PATH, f'assets/graphics/monsters/{monster_name}/')

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(full_path + animation)
    
    def get_player_distance_and_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        self.distance = self.get_player_distance_and_direction(player)[0]

        if self.distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif self.distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, attack_type = self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_type == 'weapon' or 'fist':
                self.health -= player.get_full_weapon_damage()
                self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    
    def check_death(self):
        if self.health <= 0:
            self.add_exp(monster_data[self.monster_name]['exp'])
            self.kill()
    
    def attack_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
            

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.attack_cooldown()
        self.check_death()
        
    
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)