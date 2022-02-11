import pygame
from config import *

class Upgrade_menu:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(self.player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.max_values = list(self.player.max_stats.values())

        self.height = self.display_surface.get_size()[1] * 0.8 
        self.width = self.display_surface.get_size()[0] // 6

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.create_items()

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number -1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
    
    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True
    
    def create_items(self):
        self.item_list = []
        full_width = self.display_surface.get_size()[0]

        for index, item in enumerate(range(self.attribute_number)):
            top  = self.display_surface.get_size()[1] * 0.1
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2

            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)
    
    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):

            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, 0, name, value, max_value, cost)

class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font
        self.selected = False
    
    def display_names(self, surface, name, cost, selected):
        title_surf = self.font.render(name, False, TEXT_COLOR)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        cost_surf = self.font.render(str(cost), False, TEXT_COLOR)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0, -20))
    
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)
    
    def display(self, surface, selection_num, name, value, max_value, cost):
        self.selected = True if self.index == selection_num else False
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface, name, cost, self.selected)