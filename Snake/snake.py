import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
pygame.init()
# VARIABLES

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# END VARIABLES

class cube(object):
    rows = 200
    w = 500
    def __init__(self,start,dirnx=0,dirny=0,color=RED):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos(self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, BLACK, circleMiddle, radius)
            pygame.draw.circle(surface, BLACK, circleMiddle2, radius)
        

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    self.reset((10, 10))
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    self.reset((10, 10))
                elif c.dirnx == 1 and c.pos[1] >= c.rows - 1:
                    self.reset((10, 10))
                elif c.dirnx == -1 and c.pos[1] <= 0:
                    self.reset((10, 10))
                else:
                    c.move(c.dirnx, c.dirny)
    def reset(self, pos):
        pass

    def addCube(self):
        pass
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeGap = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x += sizeGap
        y += sizeGap

        pygame.draw.line(surface, WHITE, (x, 0), (x, w))
        pygame.draw.line(surface, WHITE, (0, y), (w, y))

def redrawWindow(surface):
    global rows, width, s
    surface.fill(BLACK)
    s.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body  # Get all the posisitons of cubes in our snake

    while True:  # Keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            # This wll check if the position we generated is occupied by the snake
            continue
        else:
            break
        
    return (x,y)


def message_box(subject, content):
    pass


def main():
    global width, rows, s
    width = 500
    height = 500
    rows = 20
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((width, height))
    s = snake(RED, (10, 10))
    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        snack = cube(randomSnack(rows, s), color=GREEN)
        redrawWindow(win)

rows = 0
w = 0
h = 0

cube.rows = rows
cube.w = w


main()