import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(r'C:\Users\ested\Documents\Programming\Python_Games\Zelda2D\assets\rock.png').convert_alpha()
        self.rect  = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)