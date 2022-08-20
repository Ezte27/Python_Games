import pygame
import pathlib
from os import walk

def import_folder(path):
    surface_list = []

    for folder_name, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)


    return surface_list