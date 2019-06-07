from collections import OrderedDict

import easygui as easygui
import pygame
import random
from pip._vendor.urllib3.connectionpool import xrange

from Cell import Cell
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()
display_instructions = True
instruction_page = 1
speed = 10  # how many iterations per second
frame = 0
font = pygame.font.Font(None, 20)
imgs = ["res/alive_8.png", "res/dead_8.png", 8]
# -----CONFIG-----
myvar = easygui.enterbox("Declare Grid size x")
map_sizex = int(myvar)
myvar = easygui.enterbox("Declare number of iterations")
map_sizey = int(myvar)
width = map_sizex * imgs[2]
height = map_sizey * imgs[2]
screen_size = width, height

screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()
alive = pygame.image.load(imgs[0]).convert()
dead = pygame.image.load(imgs[1]).convert()
done = False
RULE = 30
rule30 = [0,0,0,1,1,1,1,0]
rule60 = [0,0,1,1,1,1,0,0]
rule90 = [0,1,0,1,1,0,1,0]
rule120 = [0,1,1,1,1,0,0,0]
rule225 = [1,1,1,0,0,0,0,1]

def cell_list():
    lst = []
    for i in xrange(map_sizex):
        lst.append([])
        for g in xrange(map_sizey): lst[i].append(
            (board.map[i][g].location[0] * imgs[2], board.map[i][g].location[1] * imgs[2]))
    return lst


class Board:

    def __init__(self):
        self.map = []


    def fill(self, ran):
        for i in xrange(map_sizex):
            self.map.append([])
            for g in xrange(map_sizey):
                if ran:
                    a = random.randint(0, 4)
                    if a == 0:
                        self.map[i].insert(g, Cell((i, g), True))
                    else:
                        self.map[i].insert(g, Cell((i, g)))
                else:
                    self.map[i].insert(g, Cell((i, g)))

    def draw(self):
        for i in xrange(map_sizex):
            for g in xrange(map_sizey):
                cell = self.map[i][g]
                loc = cell.location
                if cell.alive:
                    screen.blit(alive, (loc[0] * imgs[2], loc[1] * imgs[2]))
                else:
                    screen.blit(dead, (loc[0] * imgs[2], loc[1] * imgs[2]))

    def update(self):
        for i in xrange(map_sizex):
            for g in xrange(map_sizey):
                cell = self.map[i][g]
                loc = cell.location
                if cell.to_be is not None:
                    cell.alive = cell.to_be
                if self.map[i][g].alive:
                    screen.blit(alive, (loc[0] * imgs[2], loc[1] * imgs[2]))
                else:
                    screen.blit(dead, (loc[0] * imgs[2], loc[1] * imgs[2]))
                cell.to_be = None

    def get_cells(self, cell, rule):
        b = []
        cell_loc = cell.location
        b.append(self.map[(cell_loc[0] - 1)%map_sizex][frame].alive)
        b.append(self.map[cell_loc[0]%map_sizex][frame].alive)
        b.append(self.map[(cell_loc[0] + 1)%map_sizex][frame].alive)
        c = b[0] * 4 + b[1] * 2 + b[2] * 1
        if rule == 30:
            self.map[cell_loc[0]][frame+1].to_be = rule30[abs(c-7)]
        elif rule == 60:
            self.map[cell_loc[0]][frame + 1].to_be = rule60[abs(c - 7)]
        elif rule == 90:
            self.map[cell_loc[0]][frame + 1].to_be = rule90[abs(c - 7)]
        elif rule == 120:
            self.map[cell_loc[0]][frame + 1].to_be = rule120[abs(c - 7)]
        elif rule == 225:
            self.map[cell_loc[0]][frame + 1].to_be = rule225[abs(c - 7)]

    def update_frame(self):
        global frame
        for i in xrange(map_sizex):
            cell = self.map[i][frame]
            self.get_cells(cell, RULE)
        frame += 1


board = Board()

board.fill(False)
board.draw()
tp = 0
run = False

while not done:
    milliseconds = clock.tick(60)
    seconds = milliseconds / 1000.0
    tp += milliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = not run

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                run = False
                board.update_frame()
                board.update()

        if event.type ==pygame.MOUSEBUTTONUP:
            for i in xrange(map_sizex):
                for g in xrange(map_sizey):
                    board.map[i][g].pressed = False

    pressed = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    if pressed[pygame.K_r]:
        board.map = []
        board.fill(False)
        board.draw()
        frame = 0
        run = False

    if pressed[pygame.K_1]:
        RULE = 30
    if pressed[pygame.K_2]:
        RULE = 60
    if pressed[pygame.K_3]:
        RULE = 90
    if pressed[pygame.K_4]:
        RULE = 120
    if pressed[pygame.K_5]:
        RULE = 225
    if run == True and frame < map_sizey-1 and tp >= 1000 / speed:
        tp = 0
        board.update_frame()
        board.update()
    if mouse[0]:  # makes cells alive
        rects = cell_list()
        for i in xrange(map_sizex):
            if rects[i][0][0] <= pos[0] < rects[i][0][0] + imgs[2] and rects[i][0][1] <= pos[1] < \
                    rects[i][0][1] + imgs[2] and board.map[i][0].pressed is False:
                board.map[i][0].alive = True
                board.map[i][0].pressed = True
                board.update()
    if mouse[2]:  # kills cells
        rects = cell_list()
        for i in xrange(map_sizex):
            if rects[i][0][0] <= pos[0] < rects[i][0][0] + imgs[2] and rects[i][0][1] <= pos[1] < \
                    rects[i][0][1] + imgs[2] and board.map[i][0].pressed is False:
                board.map[i][0].alive = False
                board.map[i][0].pressed = False
                board.update()

    pygame.display.flip()

pygame.quit()