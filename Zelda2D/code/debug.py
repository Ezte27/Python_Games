import pygame
pygame.init()
font = pygame.font.Font(None, 30)
from config import WIDTH, HEIGHT

def debug(info, y = 10, x = WIDTH - 10, BGcolor = 'Black', TextColor = 'White'):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, TextColor)
    debug_rect = debug_surf.get_rect(topright=(x,y))
    pygame.draw.rect(display_surface, BGcolor, debug_rect)
    display_surface.blit(debug_surf, debug_rect)