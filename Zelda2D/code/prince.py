import pygame
from entity import Entity

class Princ(Entity):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphics setup
        self.image = pygame.image.load('Zelda2D/assets/graphics/CamilaFeature/prince.png').convert_alpha()
        #movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.speed = 5.5
        self.obstacles = obstacles
        self.notice_radius = 200
    
    def get_player_distance_and_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance < self.notice_radius:
            direction = (player_vec - enemy_vec).normalize() * -1
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        self.distance = self.get_player_distance_and_direction(player)[0]
        if self.distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self, player):
        if self.status == 'move':
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def update(self):
        self.move(self.speed)
        
    
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)