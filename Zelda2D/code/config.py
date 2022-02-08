#Game Setup
WIDTH    = 1280
HEIGHT   = 720
FPS      = 40
TILESIZE = 64
TITLE    = 'ZELDA 2D'
HITBOX_OFFSET = {
	'player': -26,
	'object': -60,
	'grass': -10,
	'invisible': 0,
    'tree': -55
    }
TREE_HEALTH = 3

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'Zelda2D/assets/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'Zelda2D/assets/graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'Zelda2D/assets/graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'Zelda2D/assets/graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'Zelda2D/assets/graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'Zelda2D/assets/graphics/weapons/sai/full.png'}}