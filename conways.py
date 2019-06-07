from collections import OrderedDict

import easygui as easygui
import pygame
import random
from pip._vendor.urllib3.connectionpool import xrange

from Cell import Cell
pygame.init()

speed = 10  # how many iterations per second
# -----CONFIG-----
map_sizey =1000
map_sizex =1000
while map_sizex>150:
    myvar = easygui.enterbox("Declare Grid size x(max 150)")
    map_sizex = int(myvar)
while map_sizey > 90:
    myvar = easygui.enterbox("Declare Grid size y(max 90)")
    map_sizey = int(myvar)
if map_sizey > 40 or map_sizex > 100:
    imgs = ["res/blue_8.png", "res/dead_8.png", 8]
else:
    imgs = ["res/blue_16.png", "res/dead_16.png", 8]
width = map_sizex * imgs[2]
height = map_sizey * imgs[2]
screen_size = width, height

screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()
alive = pygame.image.load(imgs[0]).convert()
dead = pygame.image.load(imgs[1]).convert()
done = False


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

    def fillOscilator(self):
        for i in xrange(map_sizex):
            self.map.append([])
            for g in xrange(map_sizey):
                self.map[i].insert(g, Cell((i, g)))
        self.map[4][4].alive = True
        self.map[5][4].alive = True
        self.map[6][4].alive = True

    def fillGlider(self):
        for i in xrange(map_sizex):
            self.map.append([])
            for g in xrange(map_sizey):
                self.map[i].insert(g, Cell((i, g)))
        self.map[4][6].alive = True
        self.map[5][4].alive = True
        self.map[5][6].alive = True
        self.map[6][5].alive = True
        self.map[6][6].alive = True

    def fillStatic(self):
        for i in xrange(map_sizex):
            self.map.append([])
            for g in xrange(map_sizey):
                self.map[i].insert(g, Cell((i, g)))
        self.map[4][4].alive = True
        self.map[5][4].alive = True
        self.map[4][5].alive = True
        self.map[5][5].alive = True

        self.map[15][15].alive = True
        self.map[15][16].alive = True
        self.map[16][14].alive = True
        self.map[16][17].alive = True
        self.map[17][14].alive = True
        self.map[17][17].alive = True
        self.map[18][15].alive = True
        self.map[18][16].alive = True

    def draw(self):
        for i in xrange(map_sizex):
            for g in xrange(map_sizey):
                cell = self.map[i][g]
                loc = cell.location
                if cell.alive:
                    screen.blit(alive, (loc[0] * imgs[2], loc[1] * imgs[2]))
                else:
                    screen.blit(dead, (loc[0] * imgs[2], loc[1] * imgs[2]))

    def get_cells(self, cell):  # gets the cells around a cell
        mapa = self.map
        a = []
        b = []
        c = 0
        cell_loc = cell.location
        try:
            a.append(mapa[abs(cell_loc[0] - 1)%map_sizex][abs(cell_loc[1] - 1)%map_sizey].location)
        except Exception:
            pass
        try:
            a.append(mapa[abs(cell_loc[0])%map_sizex][abs(cell_loc[1] - 1)%map_sizey].location)
        except Exception:
            pass
        try:
            a.append(mapa[abs(cell_loc[0] + 1)%map_sizex][abs(cell_loc[1] - 1)%map_sizey].location)
        except Exception:
            pass
        try:
            a.append(mapa[abs(cell_loc[0] - 1)%map_sizex][abs(cell_loc[1])%map_sizey].location)
        except Exception:
            pass
        try:
            a.append(mapa[abs(cell_loc[0] + 1)%map_sizex][abs(cell_loc[1])%map_sizey].location)
        except Exception:
            pass
        try:
            a.append(mapa[abs(cell_loc[0] - 1)%map_sizex][abs(cell_loc[1] + 1)%map_sizey].location)
        except Exception:
            pass
        try:
            a.append(mapa[abs(cell_loc[0])%map_sizex][abs(cell_loc[1] + 1)%map_sizey].location)
        except Exception:
            pass
        try:
            a.append(mapa[abs(cell_loc[0] + 1)%map_sizex][abs(cell_loc[1] + 1)%map_sizey].location)
        except Exception:
            pass
        num = len(list(OrderedDict.fromkeys(a)))  # removes duplicates
        for i in xrange(len(a)):
            b.append(mapa[a[i][0]][a[i][1]].alive)
        for i in b:  # c houses how many cells are alive around it
            if i:
                c += 1
        if cell.alive:  # rules
            if c < 2:
                cell.to_be = False
            if c > 3:
                cell.to_be = False
        else:
            if c == 3:
                cell.to_be = True
            # rules

    def update_frame(self):
        for i in xrange(map_sizex):
            for g in xrange(map_sizey):
                cell = self.map[i][g]
                self.get_cells(cell)

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


def cell_list():
    lst = []
    for i in xrange(map_sizex):
        lst.append([])
        for g in xrange(map_sizey): lst[i].append(
            (board.map[i][g].location[0] * imgs[2], board.map[i][g].location[1] * imgs[2]))
    return lst


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
    if pressed[pygame.K_4]:
        board.map = []
        board.fill(True)
        board.draw()
    if pressed[pygame.K_1]:
        board.map = []
        board.fillGlider()
        board.draw()
    if pressed[pygame.K_2]:
        board.map = []
        board.fillStatic()
        board.draw()
    if pressed[pygame.K_3]:
        board.map = []
        board.fillOscilator()
        board.draw()

    if run == True and tp >= 1000 / speed:
        tp = 0
        board.update_frame()
        board.update()

    if mouse[0]:  # makes cells alive
        rects = cell_list()
        for i in xrange(map_sizex):
            for g in xrange(map_sizey):
                if rects[i][g][0] <= pos[0] < rects[i][g][0] + imgs[2] and rects[i][g][1] <= pos[1] < rects[i][g][1] + \
                        imgs[2] and board.map[i][g].pressed is False:
                    board.map[i][g].alive = True
                    board.map[i][g].pressed = True
                    board.update()

    if mouse[2]:  # kills cells
        rects = cell_list()
        for i in xrange(map_sizex):
            for g in xrange(map_sizey):
                if rects[i][g][0] <= pos[0] < rects[i][g][0] + imgs[2] and rects[i][g][1] <= pos[1] < \
                        rects[i][g][1] + imgs[2] and board.map[i][g].pressed is False:
                    board.map[i][g].alive = False
                    board.map[i][g].pressed = False
                    board.update()

    pygame.display.flip()

pygame.quit()
