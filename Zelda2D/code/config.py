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
    'tree': -55,
	'spirit': -10,
	'bamboo': -25,
	'squid': -25,
	'raccoon': -120
    }
TREE_HEALTH = 100

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

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'Zelda2D/assets/graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'Zelda2D/assets/graphics/weapons/lance/full.png'},
	'axe':   {'cooldown': 300, 'damage': 20, 'graphic':'Zelda2D/assets/graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 55, 'damage': 8, 'graphic':'Zelda2D/assets/graphics/weapons/rapier/full.png'},
	'sai':   {'cooldown': 80, 'damage': 10, 'graphic':'Zelda2D/assets/graphics/weapons/sai/full.png'},
	'fist':  {'cooldown': 50, 'damage': 3, 'graphic':'Zelda2D/assets/graphics/weapons/fist/full.png'}}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':20,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':100,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 450},
	'spirit': {'health': 100,'exp':25,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':12,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}