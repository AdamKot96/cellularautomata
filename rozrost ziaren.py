import math
import tkinter as tk
from statistics import mode
from collections import Counter, OrderedDict
from Cell import Cell
import pygame
from pip._vendor.urllib3.connectionpool import xrange
import random
import _winapi
master = tk.Tk()
pygame.init()
v1 = tk.IntVar()
v1.set(0)
v2 = tk.IntVar()
v2.set(0)
v3 = tk.IntVar()
v3.set(0)
tk.Label(master, text="""Podaj rozmiary siatki""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()
e1 = tk.Entry(master)
e1.pack()
e1.insert(0, '0')

e2 = tk.Entry(master)
e2.pack()
e2.insert(0, '0')
width = 1
height = 1
screen_size = width, height

screen = pygame.display.set_mode(screen_size)
map_sizey = 0
map_sizex = 0
ilosc_ziaren = 0
imgs = ["res/dead_8.png", "res/yellow_8.png", "res/blue_8.png", "res/green_8.png", "res/lgreen_8.png",
        "res/orange_8.png", "res/pink_8.png", "res/purple_8.png", "res/red_8.png", "res/white_8.png", 8]

imgs2 = ["res/blue_8.png", "res/1.png", "res/2.png", "res/3.png", "res/4.png", "res/5.png", "res/6.png", "res/7.png", "res/8.png", "res/9.png",  8]
colors = []
for i in range(0, 9):
    colors.append(pygame.image.load(imgs[i]).convert())
speed = 10
colors2 = []
for i in range(0, 9):
    colors2.append(pygame.image.load(imgs2[i]).convert())
tk.Label(master, text="""Wybierz rodzaj zarodkowania""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()

zarodki = [
    ("Jednorodne"),
    ("Losowe"),
    ("Z promieniem"),
    ("Reczne")
]
warunki = [
    ("Absorbujące"),
    ("Periodyczne")
]
sasiady = [
    ("von neuman"),
    ("moore"),
    ("heksagonalne lewe"),
    ("heksagonalne prawe"),
    ("heksagonalne losowe"),
    ("pentagonalne gora"),
    ("pentagonalne dol"),
    ("pentagonalne lewo"),
    ("pentagonalne prawo"),
    ("pentagonalne losowe"),
    ("promien, srodek ciezkosci")
]
e3 = tk.Entry(master)
e4 = tk.Entry(master)

def shuffle2d(arr2d, rand=random):
    """Shuffes entries of 2-d array arr2d, preserving shape."""
    reshape = []
    data = []
    iend = 0
    for row in arr2d:
        data.extend(row)
        istart, iend = iend, iend+len(row)
        reshape.append((istart, iend))
    rand.shuffle(data)
    return [data[istart:iend] for (istart,iend) in reshape]

def cell_list(board):
    lst = []
    for i in xrange(map_sizex):
        lst.append([])
        for g in xrange(map_sizey): lst[i].append(
            (board.map[i][g].location[0] * imgs[-1], board.map[i][g].location[1] * imgs[-1]))
    return lst


def most_frequent(List):
    counter = Counter(List)
    return counter.most_common(2)[0]


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

    def fillRandom(self, ilosc):
        tmp = 0
        while tmp <= ilosc:
            x = random.randint(1, map_sizex - 2)
            y = random.randint(1, map_sizey - 2)
            if self.map[x][y].ziarno == 0:
                self.map[x][y].ziarno = tmp
                tmp += 1

    def filljednorodne(self, iloscx, iloscy):
        intervalx = int(map_sizex - 2 / iloscx)
        intervaly = int(map_sizey - 2 / iloscy)
        tmp = 0
        for i in xrange(1, map_sizex - 1, intervalx):
            for j in xrange(1, map_sizey - 1, intervaly):
                self.map[i][j].ziarno = tmp
                tmp += 1

    def fillpromien(self, ilosc, promien):
        tmp = 0
        while tmp <= ilosc:
            x = random.randint(0, map_sizex - 1)
            y = random.randint(0, map_sizey - 1)
            if self.map[x][y].ziarno == 0:
                self.map[x][y].ziarno = tmp
                tmp += 1

    def draw(self, screen):
        for i in xrange(map_sizex):
            for g in xrange(map_sizey):
                cell = self.map[i][g]
                loc = cell.location
                if cell.ziarno > 1 and cell.ziarno % 9 == 0:
                    cell.ziarno += 1
                if cell.alive:
                    screen.blit(colors[cell.ziarno % 9], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
                else:
                    screen.blit(colors[cell.ziarno % 9], (loc[0] * imgs[-1], loc[1] * imgs[-1]))

    def get_cells(self, cell, neigh):  # gets the cells around a cell
        if cell.ziarno == 0:
            mapa = self.map
            a = []
            b = []
            cell_loc = cell.location
            if neigh == 4:
                neigh = random.randint(2, 3)
            if neigh == 9:
                neigh = random.randint(5, 8)
            if neigh < 4:
                if neigh == 0 or neigh == 2 or neigh == 3:
                    if neigh == 0 or neigh == 2:
                        try:
                            a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                        except Exception:
                            pass
                        try:
                            a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                        except Exception:
                            pass
                    if neigh == 0 or neigh == 3:
                        try:
                            a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                        except Exception:
                            pass
                        try:
                            a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                        except Exception:
                            pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                except Exception:
                    pass
            else:
                if neigh == 4:
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass

                elif neigh == 5:
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                elif neigh == 6:
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                    except Exception:
                        pass
                elif neigh == 7:
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                    except Exception:
                        pass
                elif neigh == 8:
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].location)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].location)
                    except Exception:
                        pass
                elif neigh == 9:
                    promien = e4.get()
                    for i in range((cell_loc[0] - promien) % map_sizex, (cell_loc[0] + promien) % map_sizex):
                        for j in range((cell_loc[1] - promien) % map_sizey, (cell_loc[1] + promien) % map_sizey):
                            if (math.sqrt(cell_loc[0] % map_sizex - i + self.map[i][j].srodekx) ** 2 + (
                                    cell_loc[0] % map_sizex - i + self.map[i][j].srodekx) ** 2) < promien:
                                try:
                                    a.append(mapa[i][j].location)
                                except Exception:
                                    pass

            num = len(list(OrderedDict.fromkeys(a)))
            for i in xrange(len(a)):
                if mapa[a[i][0]][a[i][1]].ziarno != 0:
                    b.append(mapa[a[i][0]][a[i][1]].ziarno)
            if b:
                # if most_frequent(b)[0] != most_frequent(b)[1]:
                tmp = most_frequent(b)[0]
                self.map[cell_loc[0]][cell_loc[1]].ziarnotobe = tmp

    def update_frame(self, border):
        if border:
            for i in xrange(map_sizex):
                for g in xrange(map_sizey):
                    cell = self.map[i][g]
                    self.get_cells(cell, v3.get())
        else:
            for i in xrange(1, map_sizex - 1):
                for g in xrange(1, map_sizey - 1):
                    cell = self.map[i][g]
                    self.get_cells(cell, v3.get())

    def update(self, border, screen):
        if border:
            for i in xrange(map_sizex):
                for g in xrange(map_sizey):
                    cell = self.map[i][g]
                    cell.ziarno = cell.ziarnotobe
                    loc = cell.location
                    screen.blit(colors[cell.ziarno % 9], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
        else:
            for i in xrange(1, map_sizex - 1):
                for g in xrange(1, map_sizey - 1):
                    cell = self.map[i][g]
                    cell.ziarno = cell.ziarnotobe
                    loc = cell.location
                    screen.blit(colors[cell.ziarno % 9], (loc[0] * imgs[-1], loc[1] * imgs[-1]))

    def update_frame_montecarlo(self, border):
        if border:
            for i in xrange(map_sizex):
                for g in xrange(map_sizey):
                    cell = self.map[i][g]
                    self.calculateEnergy(cell)
        else:
            for i in xrange(1, map_sizex - 1):
                for g in xrange(1, map_sizey - 1):
                    cell = self.map[i][g]
                    self.calculateEnergy(cell)

    def update_montecarlo(self, border, screen):
        if border:
            for i in xrange(map_sizex):
                for g in xrange(map_sizey):
                    cell = self.map[i][g]
                    cell.energia = cell.energiatobe
                    loc = cell.location
                    if cell.eneriga > 1:
                        screen.blit(colors2[1], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
                    else:
                        screen.blit(colors2[2], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
        else:
            for i in xrange(1, map_sizex - 1):
                for g in xrange(1, map_sizey - 1):
                    cell = self.map[i][g]
                    cell.energia = cell.energiatobe
                    loc = cell.location
                    if cell.eneriga > 1:
                        screen.blit(colors2[1], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
                    else:
                        screen.blit(colors2[2], (loc[0] * imgs[-1], loc[1] * imgs[-1]))

    def calculateEnergy(self, cell, neigh,get):
        mapa = self.map
        a = []
        b = []
        cell_loc = cell.location
        if neigh == 4:
            neigh = random.randint(2, 3)
        if neigh == 9:
            neigh = random.randint(5, 8)
        if neigh < 4:
            if neigh == 0 or neigh == 2 or neigh == 3:
                if neigh == 0 or neigh == 2:
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                    except Exception:
                        pass
                if neigh == 0 or neigh == 3:
                    try:
                        a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                    except Exception:
                        pass
                    try:
                        a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                    except Exception:
                        pass
            try:
                a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
            except Exception:
                pass
            try:
                a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
            except Exception:
                pass
            try:
                a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
            except Exception:
                pass
            try:
                a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
            except Exception:
                pass
        else:
            if neigh == 4:
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass

            elif neigh == 5:
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
            elif neigh == 6:
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                except Exception:
                    pass
            elif neigh == 7:
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                except Exception:
                    pass
            elif neigh == 8:
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey].ziarno)
                except Exception:
                    pass
                try:
                    a.append(mapa[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey].ziarno)
                except Exception:
                    pass
            elif neigh == 9:
                promien = e4.get()
                for i in range((cell_loc[0] - promien) % map_sizex, (cell_loc[0] + promien) % map_sizex):
                    for j in range((cell_loc[1] - promien) % map_sizey, (cell_loc[1] + promien) % map_sizey):
                        if (math.sqrt(cell_loc[0] % map_sizex - i + self.map[i][j].srodekx) ** 2 + (
                                cell_loc[0] % map_sizex - i + self.map[i][j].srodekx) ** 2) < promien:
                            try:
                                a.append(mapa[i][j].location)
                            except Exception:
                                pass

        energy = [i for i in a if not i == mapa[(cell_loc[0]) % map_sizex][(cell_loc[1]) % map_sizey].ziarno]
        if not get:
            self.map[cell_loc[0]][cell_loc[1]].energiatobe = len(energy)

        return len(energy)

    def dispenergy(self, disp, border, screen):
        if disp:
            if border:
                for i in xrange(map_sizex):
                    for g in xrange(map_sizey):
                        cell = self.map[i][g]
                        cell.energia = cell.energiatobe
                        loc = cell.location
                        # if cell.energia > 1:
                        #     screen.blit(colors2[1], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
                        # else:
                        #     screen.blit(colors2[2], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
                        screen.blit(colors2[cell.energia], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
            else:
                for i in xrange(1, map_sizex - 1):
                    for g in xrange(1, map_sizey - 1):
                        cell = self.map[i][g]
                        cell.energia = cell.energiatobe
                        loc = cell.location
                        # if cell.energia > 1:
                        #     screen.blit(colors2[1], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
                        # else:
                        #     screen.blit(colors2[2], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
                        screen.blit(colors2[cell.energia], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
        else:
            if border:
                for i in xrange(map_sizex):
                    for g in xrange(map_sizey):
                        cell = self.map[i][g]
                        cell.ziarno = cell.ziarnotobe
                        loc = cell.location
                        screen.blit(colors[cell.ziarno % 9], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
            else:
                for i in xrange(1, map_sizex - 1):
                    for g in xrange(1, map_sizey - 1):
                        cell = self.map[i][g]
                        cell.ziarno = cell.ziarnotobe
                        loc = cell.location
                        screen.blit(colors[cell.ziarno % 9], (loc[0] * imgs[-1], loc[1] * imgs[-1]))
    def montecarlo(self,kt,iterations,neigh):
        map1 = self.map
        maparandom = map1
        maparandom = shuffle2d(maparandom)
        for i in range(0,iterations):
            for i in xrange(1, map_sizex - 1):
                for g in xrange(1, map_sizey - 1):
                    a = []
                    cell = maparandom[i][g]
                    cell_loc = cell.location
                    if neigh == 4:
                        neigh = random.randint(2, 3)
                    if neigh == 9:
                        neigh = random.randint(5, 8)
                    if neigh < 4:
                        if neigh == 0 or neigh == 2 or neigh == 3:
                            if neigh == 0 or neigh == 2:
                                try:
                                    a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                                except Exception:
                                    pass
                                try:
                                    a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                                except Exception:
                                    pass
                            if neigh == 0 or neigh == 3:
                                try:
                                    a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                                except Exception:
                                    pass
                                try:
                                    a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                                except Exception:
                                    pass
                        try:
                            a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                        except Exception:
                            pass
                        try:
                            a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey])
                        except Exception:
                            pass
                        try:
                            a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey])
                        except Exception:
                            pass
                        try:
                            a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                        except Exception:
                            pass
                    else:
                        if neigh == 4:
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass

                        elif neigh == 5:
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                        elif neigh == 6:
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                            except Exception:
                                pass
                        elif neigh == 7:
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] + 1) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                            except Exception:
                                pass
                        elif neigh == 8:
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1]) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0] - 1) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] + 1) % map_sizey])
                            except Exception:
                                pass
                            try:
                                a.append(map1[(cell_loc[0]) % map_sizex][(cell_loc[1] - 1) % map_sizey])
                            except Exception:
                                pass
                        elif neigh == 9:
                            promien = e4.get()
                            for i in range((cell_loc[0] - promien) % map_sizex, (cell_loc[0] + promien) % map_sizex):
                                for j in range((cell_loc[1] - promien) % map_sizey,
                                               (cell_loc[1] + promien) % map_sizey):
                                    if (math.sqrt(cell_loc[0] % map_sizex - i + self.map[i][j].srodekx) ** 2 + (
                                            cell_loc[0] % map_sizex - i + self.map[i][j].srodekx) ** 2) < promien:
                                        try:
                                            a.append(map1[i][j].location)
                                        except Exception:
                                            pass
                    before = cell.energia
                    choice = random.choice(a)
                    after = self.calculateEnergy(choice, neigh, True)
                    deltaE = after - before
                    if deltaE <= 0:
                        probability = 1
                    else:
                        probability = math.exp(-(deltaE/kt))
                    decision = random.random()
                    if decision <= probability:
                        self.map[cell_loc[0]%map_sizex][cell_loc[1]%map_sizey].ziarnotobe = choice.ziarno
        print("finished")

def go():
    moore = False
    done = False
    global map_sizex
    global map_sizey
    global ilosc_ziaren
    map_sizey = int(e2.get())
    if map_sizey > 90:
        map_sizey = 90
    map_sizex = int(e1.get())
    if map_sizex > 170:
        map_sizex = 170
    ilosc_ziaren = int(e3.get())
    if ilosc_ziaren < 1:
        ilosc_ziaren = 1
    promien = int(e4.get())
    if promien < 1:
        promien = 1
    iterations = int(e6.get())
    if iterations < 1:
        iterations = 1
    kt = float(e7.get())
    if kt < 0.1 or kt > 6:
        kt = 0.1
    width = map_sizex * imgs[-1]
    height = map_sizey * imgs[-1]
    screen_size = width, height
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    reczne = False
    disp = True;
    licznik = 0
    board = Board()
    board.fill(False)
    if int(v1.get()) == 0:
        board.filljednorodne(ilosc_ziaren, promien)
    elif int(v1.get()) == 1:
        board.fillRandom(ilosc_ziaren)
    elif int(v1.get()) == 2:
        board.fillpromien(ilosc_ziaren, promien)
    elif int(v1.get()) == 3:
        reczne = True


    board.draw(screen)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    for i in xrange(map_sizex):
                        for g in xrange(map_sizey):
                            cell = board.map[i][g]
                            board.calculateEnergy(cell, v3.get(),False)
                    board.dispenergy(disp, v2.get(),screen)
                    disp = not disp
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    board.montecarlo(kt,iterations, v3.get())
                    board.update(v2.get(), screen)
            if event.type == pygame.MOUSEBUTTONUP:
                for i in xrange(map_sizex):
                    for g in xrange(map_sizey):
                        board.map[i][g].pressed = False

        pressed = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        if run == True and tp >= 1000 / speed:
            tp = 0
            board.update_frame(v2.get)
            board.update(v2.get(), screen)

        if reczne:

            if mouse[0]:  # makes cells alive
                rects = cell_list(board)
                for i in xrange(map_sizex):
                    for g in xrange(map_sizey):
                        if rects[i][g][0] <= pos[0] < rects[i][g][0] + imgs[-1] and rects[i][g][1] <= pos[1] < \
                                rects[i][g][
                                    1] + \
                                imgs[-1] and board.map[i][g].pressed is False:
                            licznik += 1
                            board.map[i][g].ziarno = licznik
                            board.map[i][g].ziarnotobe = licznik
                            board.map[i][g].pressed = True
                            board.update(v2.get(), screen)

            if mouse[2]:  # kills cells
                rects = cell_list(board)
                for i in xrange(map_sizex):
                    for g in xrange(map_sizey):
                        if rects[i][g][0] <= pos[0] < rects[i][g][0] + imgs[-1] and rects[i][g][1] <= pos[1] < \
                                rects[i][g][1] + imgs[-1] and board.map[i][g].pressed is False:
                            licznik -= 1
                            board.map[i][g].ziarno = 0
                            board.map[i][g].ziarnotobe = 0
                            board.map[i][g].pressed = False
                            board.update(v2.get(), screen)

        pygame.display.flip()

    pygame.quit()


for val1, zarodek in enumerate(zarodki):
    tk.Radiobutton(master,
                   text=zarodek,
                   indicatoron=0,
                   width=40,
                   padx=20,
                   variable=v1,
                   value=val1).pack(anchor=tk.W)
tk.Label(master, text="""Parametry""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()
e3 = tk.Entry(master)
e3.pack()
e3.insert(0, '0')

e4 = tk.Entry(master)
e4.pack()
e4.insert(0, '0')
tk.Label(master, text="""Wybierz warunek brzegowy""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()
for val2, warunek in enumerate(warunki):
    tk.Radiobutton(master,
                   text=warunek,
                   indicatoron=0,
                   width=40,
                   padx=20,
                   variable=v2,
                   value=val2).pack(anchor=tk.W)
tk.Label(master, text="""Wybierz sąsiedztwa""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()
for val3, sasiad in enumerate(sasiady):
    tk.Radiobutton(master,
                   text=sasiad,
                   indicatoron=0,
                   width=40,
                   padx=20,
                   variable=v3,
                   value=val3).pack(anchor=tk.W)
tk.Label(master, text="""Promien""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()
e5 = tk.Entry(master)
e5.pack()
e5.insert(0, '0')
tk.Label(master, text="""Iteracje""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()
e6 = tk.Entry(master)
e6.pack()
e6.insert(0, '1')
tk.Label(master, text="""wspolczynnik kt""", font=("Helvetica", 16), justify=tk.LEFT, padx=20).pack()
e7 = tk.Entry(master)
e7.pack()
e7.insert(0, '0.1')
tk.Button(master, text="START", width=45, command=go).pack()
master.mainloop()


