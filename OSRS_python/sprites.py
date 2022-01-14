# NEW NEW EDIT ----------------------------------------------------------------------
import pygame
from config import *
import math
import time
import random

class SpriteSheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    def get_sprite(self, x, y, width, height, colorkey):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        if colorkey == "black":
            sprite.set_colorkey(BLACK)
        elif colorkey == 'white':
            sprite.set_colorkey(WHITE)
        return sprite

class Player(pygame.sprite.Sprite):
    appleCount = 0
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.has_sword = False
        self.has_axe = False
        self.has_key = False
        self.hearts = 3
        self.hit = False
        self.hit_count = 0

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height, 'black')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        Player.appleCount = 0
    
    def update(self):
        self.movement()
        self.animate()
        self.collide_apple()
        self.collide_sword()
        self.collide_axe()
        self.collide_key()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'

        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'

        if 0 <= self.rect.y <= 450 or self.rect.y == -4: # or self.rect.y == -2 or self.rect.y == -3 or self.rect.y == -4:
            if keys[pygame.K_UP]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED + 3

        if 0 <= self.rect.y <= 450 or self.rect.y == 451: # or self.rect.y == 452 or self.rect.y == 453 or self.rect.y == 454: 
            if keys[pygame.K_DOWN]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED + 3

        if 0 <= self.rect.x <= 600 or self.rect.x == -2:
            if keys[pygame.K_LEFT]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED + 3
            
        if 0 <= self.rect.x <= 600 or self.rect.x == 603:
            if keys[pygame.K_RIGHT]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED + 3
                
    
    def collide_blocks(self, direction):
        hit = []
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits2 = pygame.sprite.spritecollide(self, self.game.trees, False)
            hits3 = pygame.sprite.spritecollide(self, self.game.doors, False)

            if hits or hits2 or hits3:
                if hits:
                    hit.append(hits[0])
                elif hits2:
                    hit.append(hits2[0])
                elif hits3:
                    if hits3[0].opened:
                        return True
                    elif hits3[0].opened != True:
                        hit.append(hits3[0])

                if self.x_change > 0: # Moving Right
                    self.rect.x = hit[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x = sprite.rect.x + PLAYER_SPEED
                if self.x_change < 0: # Moving Left
                    self.rect.x = hit[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x = sprite.rect.x - PLAYER_SPEED
        hit = []
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits2 = pygame.sprite.spritecollide(self, self.game.trees, False)
            hits3 = pygame.sprite.spritecollide(self, self.game.doors, False)

            if hits or hits2 or hits3:
                if hits:
                    hit.append(hits[0])
                elif hits2:
                    hit.append(hits2[0])
                elif hits3:
                    if hits3[0].opened:
                        return True
                    elif hits3[0].opened != True:
                        hit.append(hits3[0])
                    
                if self.y_change > 0:
                    self.rect.y = hit[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y = sprite.rect.y + PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hit[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y = sprite.rect.y - PLAYER_SPEED
    
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.hit = True
        else:
            if self.hit:
                self.hearts -= 1
                self.hit = False
                if self.hearts <= 0:
                    self.kill()
                    self.game.playing = False
            
    def collide_apple(self):
        hits = pygame.sprite.spritecollide(self, self.game.apples, True)
        if hits:
            Player.appleCount += 1
            self.hearts += 1
            return True
    
    def collide_sword(self):
        if self.has_sword != True:
            hits = pygame.sprite.spritecollide(self, self.game.swords, True)
            if hits:
                self.has_sword = True
                self.has_axe = False
    
    def collide_axe(self):
        if self.has_axe != True:
            hits = pygame.sprite.spritecollide(self, self.game.axes, True)
            if hits:
                self.has_axe = True
                self.has_sword = False
    
    def collide_key(self):
        if self.has_key != True:
            hits = pygame.sprite.spritecollide(self, self.game.keys, True)
            if hits:
                self.has_key = True

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height, 'black'),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height, 'black'),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height, 'black')]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height, 'black'),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height, 'black'),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height, 'black')]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height, 'black'),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height, 'black'),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height, 'black')]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height, 'black'),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height, 'black'),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height, 'black')]
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height, 'black')
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            
        elif self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height, 'black')
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height, 'black')
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height, 'black')
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height, 'black')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class closedDoor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.opened = False
        self.pressed = False
        
        self.image = self.game.doors_spritesheet.get_sprite(0, 80, self.width, self.height, 'black')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        if self.game.player.has_key:
            self.check_click()
        if self.opened == True:
            openedDoor(self.game, self.rect.x, self.rect.y)
            self.kill()

    def check_click(self):
        if not self.pressed:
            if -64 <= abs(self.game.player.rect.x) - abs(self.rect.x) <= 64:
                if -64 <= abs(self.game.player.rect.y) - abs(self.rect.y) <= 64:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.rect.collidepoint(mouse_pos):#self.start_chest_rect <= mouse_pos <= self.end_chest_rect:
                        if pygame.mouse.get_pressed()[0]:
                            self.pressed = True
                            self.opened = True

class openedDoor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y 
        self.width = TILESIZE
        self.height = TILESIZE
        self.opened = True

        self.image = self.game.doors_spritesheet.get_sprite(32, 80, self.width, self.height, 'black')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.trees
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.health = 5

        self.image = self.game.tree_spritesheet.get_sprite(0, 8, self.width + 12, self.height*2, 'black')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, loot):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image_option = image
        self.loot = loot
        
        self.pressed = False
        self.chest_content = ['random', 'coin', 'sword', 'key', 'axe']  
        self.content = self.chest_content[self.loot]

        if image == 0:
            self.image = self.game.chest_spritesheet.get_sprite(0, 0, self.width, self.height, 'black')
        elif image == 1:
            self.image = self.game.chest_spritesheet.get_sprite(32, 0, self.width, self.height, 'black')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.image_option == 0:
            self.check_click()
        else:
            pass

    def check_click(self):
        if not self.pressed:
            self.start_chest_rect = (self.rect.x, self.rect.y)
            self.end_chest_rect = (self.rect.x + TILESIZE, self.rect.y + TILESIZE)
            if -64 <= abs(self.game.player.rect.x) - abs(self.start_chest_rect[0]) <= 64:
                if -64 <= abs(self.game.player.rect.y) - abs(self.start_chest_rect[1]) <= 64:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.rect.collidepoint(mouse_pos):#self.start_chest_rect <= mouse_pos <= self.end_chest_rect:
                        if pygame.mouse.get_pressed()[0]:
                            self.pressed = True
                            if self.content == 'sword':
                                Sword(self.game, self.start_chest_rect[0], self.start_chest_rect[1])
                            elif self.content == 'coin':
                                pass
                            elif self.content == 'key':
                                Key(self.game, self.start_chest_rect[0], self.start_chest_rect[1])
                            elif self.content == 'axe':
                                Axe(self.game, self.start_chest_rect[0], self.start_chest_rect[1])
                            elif self.content == 'random':
                                randnum = random.randint(1, len(self.chest_content) - 1)
                                content = self.chest_content[randnum]
                                if content == 'sword':
                                    Sword(self.game, self.start_chest_rect[0] // TILESIZE - 1, self.start_chest_rect[1] // TILESIZE)
                                elif content == 'coin':
                                    pass
                                elif content == 'key':
                                    pass
                                elif content == 'axe':
                                    Axe(self.game, self.start_chest_rect[0] // TILESIZE - 1, self.start_chest_rect[1] // TILESIZE)
                            #Chest(self.game, int(math.floor(self.start_mouse_rect[0] / TILESIZE)) + 1, int(math.floor(self.start_mouse_rect[1] / TILESIZE)), 1)
                            self.kill()
                            #print(f'{int(math.floor(self.start_mouse_rect[0] / TILESIZE))} ---- {int(math.floor(self.start_mouse_rect[1] / TILESIZE))}')
                            #print('Clicked!')
                else:
                    pass

class Grass(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.terrain_list = [(64, 352), (64, 352), (64, 352), (64, 352), (128, 352), (0, 352), (0, 352), (448, 352)]
        self.choice = random.randint(0, 6)
        self.terrain = self.terrain_list[self.choice]

        self.image = self.game.terrain_spritesheet.get_sprite(self.terrain[0], self.terrain[1], self.width, self.height, 'black')
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self.screen = self.game.screen
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.animation_loop = 1
        self.movement_loop = 0
        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.max_travel = random.randint(30, 80)
        self.max_travel_finished = False
        self.hearts = 3
        self.hitted = False

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height, 'black')
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change
        self.collide_blocks('y')


        self.x_change = 0
        self.y_change = 0
        if self.max_travel_finished:
            self.facing = random.choice(['left', 'right', 'up', 'down'])
            self.max_travel = random.randint(30, 80)
            self.movement_loop = 0
            self.max_travel_finished = False
    
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED - 1
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.max_travel_finished = True
        elif self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.max_travel_finished = True
        elif self.facing == 'up':
            self.y_change -= ENEMY_SPEED - 1
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.max_travel_finished = True
        elif self.facing == 'down':
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.max_travel_finished = True
    
    def animate(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height, 'black'),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height, 'black'),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height, 'black')]

        up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height, 'black'),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height, 'black'),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height, 'black')]

        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height, 'black'),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height, 'black'),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height, 'black')]

        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height, 'black'),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height, 'black'),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height, 'black')]
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height, 'black')
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height, 'black')
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height, 'black')
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height, 'black')
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
    
    def collide_blocks(self, direction):
        hit = []
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits2 = pygame.sprite.spritecollide(self, self.game.trees, False)
            hits3 = pygame.sprite.spritecollide(self, self.game.doors, False)

            if hits or hits2 or hits3:
                if hits:
                    hit.append(hits[0])
                elif hits2:
                    hit.append(hits2[0])
                elif hits3:
                    hit.append(hits3[0])
                if self.x_change > 0: # Moving Right
                    self.rect.x = hit[0].rect.left - self.rect.width
                if self.x_change < 0: # Moving Left
                    self.rect.x = hit[0].rect.right
        
        hit = []
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits2 = pygame.sprite.spritecollide(self, self.game.trees, False)
            hits3 = pygame.sprite.spritecollide(self, self.game.doors, False)

            if hits or hits2 or hits3:
                if hits:
                    hit.append(hits[0])
                elif hits2:
                    hit.append(hits2[0])
                elif hits3:
                    hit.append(hits3[0])

                if self.y_change > 0:
                    self.rect.y = hit[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hit[0].rect.bottom
    
class enemyHealth(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy):
        self.game = game
        self.enemy = enemy
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemyHealthBars
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE - 10
        self.height = TILESIZE - 10

        self.image = pygame.Surface([self.width, self.height/ 4])
        self.image.fill(RED)
        self.image.blit( self.image,(self.x, self.y - self.height / 2, self.width, self.height/4))
    	
        self.rect = self.image.get_rect()
        self.rect.x = self.enemy.rect.x
        self.rect.y = self.enemy.rect.y - self.height

    def update(self):
        self.rect.x = self.enemy.rect.x
        self.rect.y = self.enemy.rect.y - self.height
        if self.enemy.hearts >= 3:
            self.image = pygame.Surface([self.width, self.height/ 4])
            self.image.fill(RED)
        elif self.enemy.hearts == 2:
            self.image = pygame.Surface([self.width/1.3, self.height/ 4])
            self.image.fill(RED)
        elif self.enemy.hearts == 1:
            self.image = pygame.Surface([self.width/2.3, self.height/ 4])
            self.image.fill(RED)
        else:
            self.image = pygame.Surface([0, self.height/ 4])
            self.image.fill(RED)
            self.kill()
    
class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font(r'C:\Users\esteb\OneDrive\Documents\Programming\pygameProjects\OSRS_python\fonts\Roboto-Medium.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg    

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def isPressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Heart(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.apples
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE - 10
        self.height = TILESIZE - 10

        self.image = self.game.apple_spritesheet.get_sprite(0, 0, self.width, self.height, 'black')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Sword(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.swords
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x #* TILESIZE
        self.y = y #* TILESIZE
        self.width = TILESIZE - 10
        self.height = TILESIZE - 10

        self.image = self.game.sword_surf
        self.rect = self.image.get_rect(topleft = (x, y))
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.screen.blit(self.image,self.rect)

class Axe(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.axes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y 
        self.width = TILESIZE 
        self.height = TILESIZE

        self.image = self.game.axe_spritesheet.get_sprite(0, 0, self.width, self.height, 'black')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Key(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.keys
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x #* TILESIZE
        self.y = y #* TILESIZE
        self.width = TILESIZE 
        self.height = TILESIZE

        self.image = self.game.keys_spritesheet.get_sprite(0, 0, self.width, self.height, 'white')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, 'black')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.hitEnemy = False

    def update(self):
        self.animate()
        if self.hitEnemy == False:
            self.collide()

    def collide(self):
        index = 0
        self.applex = self.game.player.rect.x
        self.appley = self.game.player.rect.y
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits and self.hitEnemy != True:
            index = self.game.enemyList.index(hits[0])
            print("HIT!")
            print(self.game.enemyList[index].hearts)
            if self.game.player.has_sword:
                self.game.enemyList[index].hearts -= 3
            elif self.game.player.has_axe:
                self.game.enemyList[index].hearts -= 2
            else:
                self.game.enemyList[index].hearts -= 1
            if self.game.enemyList[index].hearts <= 0:
                if random.randint(1, 3) == 2:   
                    Heart(self.game, int(self.applex // TILESIZE), int(self.appley // TILESIZE))
            self.hitEnemy = True
        else:
            self.hitEnemy = False
        if self.game.player.has_axe:
            hittree = pygame.sprite.spritecollide(self, self.game.trees, True)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height, 'black')]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height, 'black')]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height, 'black'),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height, 'black')]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, 'black'),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height, 'black'),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height, 'black'),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height, 'black'),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height, 'black')]
        
        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        elif direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        elif direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        elif direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
