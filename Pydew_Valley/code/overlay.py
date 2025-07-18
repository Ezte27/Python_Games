from settings import *
import os
import pygame

class Overlay:
    def __init__(self, player):

        # General Setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path_seed = os.path.join(PARENT_PATH,"graphics/crops/")
        overlay_path_tool = os.path.join(PARENT_PATH, "graphics/tools/")
        self.tools_surf = {tool: pygame.image.load(f"{overlay_path_tool}{tool}.png").convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f"{overlay_path_seed}{seed}/seed.png").convert_alpha() for seed in player.seeds}
    
    def display(self):
        
        # Tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # Seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)