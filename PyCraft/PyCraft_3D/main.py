# Importing libraries
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

block_pick = 1

game = Ursina() # Initializing the game

window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
    global block_pick
    if held_keys['1']: block_pick = 1
    elif held_keys['2']: block_pick = 2
    elif held_keys['3']: block_pick = 3
    elif held_keys['4']: block_pick = 4

# Entities
class Voxel(Button):
    def __init__(self, position = (0, 0, 0)):
        texture = "grass"
        if block_pick == 1: texture = "grass"
        elif block_pick == 2: texture = 'white_cube'
        elif block_pick == 3: texture = 'grass'
        elif block_pick == 4: texture = 'brick'
        super().__init__(
            parent = scene,
            model = "cube",
            position = position,
            origin_y = 0.5,
            texture = texture,
            color = color.white,
            highlight_color = color.lime,
            scale = 1
        )
    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                block = Voxel(position = self.position + mouse.normal)
            if key == "right mouse down":
                destroy(self)

for z in range(20):
    for x in range(20):
        block = Voxel(position = (x, 0, z))

player = FirstPersonController(mouse_sensitivity = Vec2(80, 80), jump_height = 1)

game.run()