# NEW NEW EDIT -----------------------------------------------------------------------------------------------
import pygame
from PIL import Image
from config import *
from sprites import *
import sys, random, json, time

mapId = 0#int(input('Choose Map: ')) - 1
with open('OSRS_python/maps.json', 'r') as f:
    data = json.load(f)
map = data['maps'][mapId]['TileMap']

image = Image.open('OSRS_python/img/Door.png')
#image = image.resize((TILESIZE, TILESIZE))
print(image.size)
#image.save(r'C:/Users/esteb/OneDrive/Documents/Programming/pygameProjects/OSRS_python/img/.png')

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('OSRS_python/Gamefonts/Roboto-Medium.ttf', 48)  
        self.heartFont = pygame.font.Font('OSRS_python/Gamefonts/Roboto-Medium.ttf', 22)
        self.running = True
        self.pressed = False
        self.timer = 0.0
        self.enemyList = []

        self.character_spritesheet = SpriteSheet('OSRS_python/img/character.png')
        self.terrain_spritesheet = SpriteSheet('OSRS_python/img/terrain.png')
        self.enemy_spritesheet = SpriteSheet('OSRS_python/img/enemy.png')
        self.intro_background = pygame.image.load('OSRS_python/img/introbackground.png')
        self.go_background = pygame.image.load('OSRS_python/img/gameover.png')
        self.sword_spritesheet = SpriteSheet('OSRS_python/img/sword.png')
        self.attack_spritesheet = SpriteSheet('OSRS_python/img/attack.png')
        self.chest_spritesheet = SpriteSheet('OSRS_python/img/chest2.png')
        self.tree_spritesheet = SpriteSheet('OSRS_python/img/Pines.png')
        self.apple_spritesheet = SpriteSheet('OSRS_python/img/apple.png')
        self.axe_spritesheet = SpriteSheet('OSRS_python/img/axe.png')
        self.keys_spritesheet = SpriteSheet('OSRS_python/img/KeyIcons.png')
        self.doors_spritesheet = SpriteSheet('OSRS_python/img/Door.png')
        self.sword_surf = self.sword_spritesheet.get_sprite(0, 0, 64, 64, 'black')
        self.axe_surf = self.axe_spritesheet.get_sprite(0, 0, 96, 96, 'black')

    def createTilemap(self):
        playerPosX = len(map[0])//2.45
        playerPosY = len(map)//2.3

        for i, row in enumerate(map): # (random.choice([Tile_Map1, Tile_Map2, Tile_Map3])):
            for j, column in enumerate(row):
                if column == "B":
                    Grass(self, j - playerPosX, i - playerPosY)
                    Block(self, j - playerPosX, i - playerPosY)


                elif column == 'C':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Chest(self, j - playerPosX, i - playerPosY, 0, 0)
                elif column == 'c':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Chest(self, j - playerPosX, i - playerPosY, 0, 2)
                elif column == '1':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Chest(self, j - playerPosX, i - playerPosY, 0, 4)
                elif column == '2':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Chest(self, j - playerPosX, i - playerPosY, 0, 3)
                elif column == '¢':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Chest(self, j - playerPosX, i - playerPosY, 0, 1)


                elif column == "P":
                    Grass(self, j - playerPosX, i - playerPosY)
                    self.player = Player(self, j - playerPosX, i - playerPosY)
                elif column == 'E':
                    Grass(self, j - playerPosX, i - playerPosY)
                    enemy = Enemy(self, j - playerPosX, i - playerPosY)
                    enemyHealth(self, j - playerPosX, i - playerPosY, enemy)
                    self.enemyList.append(enemy)
                elif column == 'A':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Heart(self, j - playerPosX, i - playerPosY)
                elif column == 'S':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Sword(self, j - playerPosX, i - playerPosY)
                elif column == '.':
                    Grass(self, j - playerPosX, i - playerPosY)
                elif column == 'T':
                    Grass(self, j - playerPosX, i - playerPosY)
                    Tree(self, j - playerPosX, i - playerPosY)
                elif column == 'D':
                    closedDoor(self, j - playerPosX, i - playerPosY)


    def new(self):
        # a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.apples = pygame.sprite.LayeredUpdates()
        self.swords = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.trees = pygame.sprite.LayeredUpdates()
        self.enemyHealthBars = pygame.sprite.LayeredUpdates()
        self.axes = pygame.sprite.LayeredUpdates()
        self.keys = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        if self.player.has_sword == True:
            timetowait = -1.4
        else:
            timetowait = -0.8
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    if self.timer - time.perf_counter() <= timetowait:
                        if self.player.facing == 'up':
                            Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                        if self.player.facing == 'down':
                            Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                        if self.player.facing == 'right':
                            Attack(self, self.player.rect.x  + TILESIZE, self.player.rect.y)
                        if self.player.facing == 'left':
                            Attack(self, self.player.rect.x  - TILESIZE, self.player.rect.y)
                        self.timer = time.perf_counter()
                if event.key == pygame.K_q:
                    self.playing = False
            for enemy in self.enemyList:
                        if enemy.hearts <= 0:
                            self.enemy = self.enemyList.pop(self.enemyList.index(enemy))
                            self.enemy.kill()
                        


    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_hearts()
        if self.player.has_sword:
            self.equipment_rect = self.sword_surf.get_rect(topleft = (25, 25))
            self.screen.blit(self.sword_surf, self.equipment_rect)
        
        elif self.player.has_axe:
            self.equipment_rect = self.axe_surf.get_rect(topleft = (25, 25))
            self.screen.blit(self.axe_surf, self.equipment_rect)
        else:
            self.hand_surf = pygame.Surface((64,64))
            self.hand_surf.fill((229, 194, 152))
            self.equipment_rect = self.hand_surf.get_rect(topleft = (25, 25))
            self.screen.blit(self.hand_surf, self.equipment_rect)
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def game_over(self):
        for i in self.enemyList:
            i.kill()
            self.enemyList.remove(i)
        intro = True

        text = self.font.render('GAME OVER', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        restart_button = Button(260, 300, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.isPressed(mouse_pos,mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro(self):
        intro = True

        title = self.font.render('Old School ScapeRun', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/3.5))

        play_button = Button(WIN_WIDTH/2.3, WIN_HEIGHT/2.5, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.isPressed(mouse_pos,mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def draw_hearts(self):
        self.hearts_text = f'Hearts left: {self.player.hearts}' 
        self.hearts_surf = self.heartFont.render(self.hearts_text, True, BLUE)
        self.heart_rect = self.hearts_surf.get_rect(topright = (WIN_WIDTH - 30, 20))
        self.screen.blit(self.hearts_surf, self.heart_rect)
    

g = Game()
g.intro()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
print(f'You collected {Player.appleCount} apples')
sys.exit()