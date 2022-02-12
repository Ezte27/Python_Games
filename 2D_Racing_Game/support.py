from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def get_sprite(path, x, y, width, height):
	spriteSheet = pygame.image.load(path).convert_alpha()
	sprite = pygame.Surface([width, height])
	sprite.blit(spriteSheet, (0,0), (x, y, width, width))
	return sprite