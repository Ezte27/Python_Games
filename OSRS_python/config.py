import random, json

WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
FPS = 60

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 2
ENEMY_SPEED = 1.2

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (32, 27, 255)
BROWN = (101, 67, 33)
WHITE = (255, 255, 255)

# ALL MAP ELEMENTS:

#P = PLAYER
#B = BLOCK
#D = DOOR
#E = ENEMY(Goblin)
#S = Sword
#C = Chest
#T = TREE
#. = GRASS

Tile_Map1 = [
        'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
        'B.............'
]

Tile_Map2 = [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..................B',
        'B...BBB...E....C...B',
        'B...T.......BB.....B',
        'B..................B',
        'B...BB........E....B',
        'B.........P........B',
        'B..................B',
        'B...E..........B...B',
        'B..................B',
        'B....B......T......B',
        'B.....B.......B....B',
        'B..........E.......B',
        'B..S...............B',
        'BBBBBBBBBBBBBBBBBBBB'
]

Tile_Map3 = [
        'BBBBBBBBBBBBBBBBBBBB',
        'B..E...........S...B',
        'B...........B......B',
        'B...B..............B',
        'B..............E...B',
        'B..................B',
        'B.........P........B',
        'B.......B..........B',
        'B..B...........B...B',
        'B............E.....B',
        'B......B...........B',
        'B.............B....B',
        'B..E...............B',
        'B..................B',
        'BBBBBBBBBBBBBBBBBBBB'
]

#  # ## # # # # ### # # # #  # ##  # # # # # #  # # # # # # ### # # # #  # ## # ##
enemyP = 1#int(input('Enemy amount: '))
blockP = 3#int(input('Block amount: '))
grassP = 90#int(input('Grass amount: '))
swordP = 0#int(input('Sword amount: '))
chestP = 0#int(input('Chest amount: '))
treeP = 3#int(input('Tree amount: '))
print('------------------------')
if swordP != 0:
        mapXSize = 50#int(input('Enter the x size for the map: '))
        mapYSize = 20#int(input('Enter the y size for the map: '))
        saveMap = 'y'#input('Save Map in a file?[y/n] ')
        TileMap = []
        tilesPerRow = ''
        player = 'P'
        randomChoice = ['E','B','.', 'S', 'C', 'T']
        for dot in range(grassP):
                randomChoice.append('.')
        for e in range(enemyP):
                randomChoice.append('E')
        for b in range(blockP):
                randomChoice.append('B')
        for s in range(swordP):
                randomChoice.append('S')
        for c in range(chestP):
                randomChoice.append('C')
        for t in range(treeP):
                randomChoice.append('T')
        
        tilesPerRow = ''
        randomLength = len(randomChoice)
        dotTile = ''
        dotTileOld = ''
        dotSpace = 0
        StartSpaceTileOld = ''
        EndSpaceTileOld = ''
        spaceMapTile = []
        spaceLength = 0
        completeSpaceRow = ''
        StartRandomNumOld = 0
        EndRandomNumOld = 0
        Start_EndOld = 0
        Start_EndNew = 0


        for line in range(mapYSize):
                StartSpaceTileNew = ''
                EndSpaceTileNew = ''
                spaceLength = 0
                dotSpace = 0
                Start_EndOld = 0
                Start_EndNew = 0
                EndSpaceLength = 0
                StartSpaceLength = 0
                dotTile = ''
                dotTileEnd = ''
                completeSpaceRow = ''
                StartRandomNum = random.randint(0, 12)
                for n in range(StartRandomNum):
                        StartSpaceTileNew += ' '
                
                EndRandomNum = random.randint(0, 12)
                for u in range(EndRandomNum):
                        EndSpaceTileNew += ' '

                spaceLength = len(StartSpaceTileNew) + len(EndSpaceTileNew)
                dotSpace = mapXSize - spaceLength #+ random.randint(5, 25)
                for m in range(3):
                        if m == 0:
                                for h in range(len(StartSpaceTileOld) - len(StartSpaceTileNew)):
                                        dotTile+='~'
                                StartSpaceTiles = - len(StartSpaceTileOld) - len(EndSpaceTileOld) + len(StartSpaceTileNew) - 2
                                if StartSpaceTiles < 0:
                                        for b in range(abs(StartSpaceTiles)):
                                                StartSpaceTileNew.replace(' ', '', 1)
                        elif m == 2:
                                
                                if len(EndSpaceTileOld) - len(EndSpaceTileNew) >= 1:
                                        for g in range(abs(len(EndSpaceTileOld) - len(EndSpaceTileNew) - len(StartSpaceTileOld) - len(StartSpaceTileNew) - 3  - len(dotTileOld) - len(dotTile) )):
                                                dotTile.replace('.', '', 1)         
                        else:
                                for q in range(dotSpace - len(dotTile)):
#                                if m == 0:
 #                                       pass
  #                              else:
   #                                     Start_EndOld = len(StartSpaceTileOld) + len(EndSpaceTileOld)
    #                                    Start_EndNew = len(StartSpaceTileNew) + len(EndSpaceTileNew)
     #                                   SpaceforBlocks = Start_EndNew - Start_EndOld 
                                        dotTile += '.'

#                if line == 0:
 #                       pass
  #              else:
   #                     if SpaceforBlocks < 0:
    #                            dotTile = dotTile.replace('.', '', abs(SpaceforBlocks))
     #                   elif SpaceforBlocks > 0:
      #                          for s in range(SpaceforBlocks):
       #                                 dotTile += '.'
        #                else:
         #                       pass
                completeSpaceRow = StartSpaceTileNew + '~' + dotTile + dotTileEnd + '~' + EndSpaceTileNew
                spaceMapTile.append(completeSpaceRow)
                StartSpaceTileOld = StartSpaceTileNew
                EndSpaceTileOld = EndSpaceTileNew
                dotTileOld = dotTile
        

        print(spaceMapTile)
        for i, row in enumerate(spaceMapTile):
                tilesPerRow = ''
                for j, column in enumerate(row):
                        if i == 0:
                                tilesPerRow += 'B'
                        elif i == len(spaceMapTile) - 1:
                                tilesPerRow += 'B'
                        else:
                                if column == '~':
                                        tilesPerRow += 'B'
                                if column == ' ':
                                        tilesPerRow += ' '
                                if column == '.':
                                        choice = random.choice(randomChoice)
                                        tilesPerRow += choice

                TileMap.append(tilesPerRow)

        print('---------------------------------------------------------------------------------------')
        print(TileMap)
        if saveMap == 'y':
                with open(r'C:\Users\esteb\OneDrive\Documents\Programming\pygameProjects\OSRS_python\maps.json', 'r') as f:
                        data = json.load(f)
                TileMapDict = {
                        "id": len(data['maps']) + 1,
                        "TileMap": TileMap
                }
                data["maps"].append(TileMapDict)
                with open(r'C:\Users\esteb\OneDrive\Documents\Programming\pygameProjects\OSRS_python\maps.json', 'w') as f:
                        json.dump(data, f, indent=4)
        else:
                pass

createMap = False
# Creating a Map
if createMap:
        #VARIABLES
        MAP_DIMS = (50, 50)
        MAP = []
        MAP_ROW = ""

        for x in range(MAP_DIMS[0]):   
                MAP_ROW += "."
        for y in range(MAP_DIMS[1]):
                MAP.append(MAP_ROW)
# Putting the player on the map
if createMap:
        #VARIABLES
        playerY = len(MAP)//2
        playerX = len(MAP_ROW)//2
        
        playerRow = MAP.pop(playerY-1)
        playerRow = list(playerRow)
        playerRow[playerX] = "P"
        playerRow = "".join(playerRow)
        MAP.insert(playerY, playerRow)

save_map = True
if save_map and createMap:
        with open(r'C:\Users\esteb\OneDrive\Documents\Programming\pygameProjects\OSRS_python\maps.json', 'r') as f:
                data = json.load(f)
                TileMapDict = {
                "id": len(data['maps']) + 1,
                "TileMap": MAP}
                data["maps"].append(TileMapDict)
        with open(r'C:\Users\esteb\OneDrive\Documents\Programming\pygameProjects\OSRS_python\maps.json', 'w') as f:
                json.dump(data, f, indent=4)
else:
        pass