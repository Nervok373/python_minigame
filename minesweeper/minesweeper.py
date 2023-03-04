import sys
import random
import time

import pygame
from pygame.locals import *


# settings
CELL_SIZE = 40
MAP_SIZE = (35, 25)
FPS = 60
BOMB = 85
TIME_START = time.time()

OPENNESS_MAP = ["c"*MAP_SIZE[0] for _ in range(MAP_SIZE[1])]
CELLS_MAP = []

text_color = (255, 255, 255)
text_size = 26
BOMB_COUNT = BOMB

background_color = "#4d5153"


def caption_update():
    t = round(time.time() - TIME_START)
    pygame.display.set_caption(
        f"Bombs: {BOMB_COUNT}     time: {round(t/60)}:"
        f"{'0'+str(t%60) if t%60 < 10 else t%60}")


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((MAP_SIZE[0]*CELL_SIZE,
                                  MAP_SIZE[1]*CELL_SIZE), DOUBLEBUF)

caption_update()
clock = pygame.time.Clock()

surface_text = pygame.Surface((200, 50))
font_text = pygame.font.SysFont('Aria', text_size)

def bomb_generate(bombs:int):
    bomb_cords = []
    while len(bomb_cords) < bombs:
        cord = ((random.randint(0, MAP_SIZE[0]-1),
                          random.randint(0, MAP_SIZE[1]-1)))

        if cord not in bomb_cords:
            bomb_cords.append(cord)

    return bomb_cords

def map_generate(size:(int, int), bombs:int):
    bomb_cords = bomb_generate(bombs)
    cells = []

    for y in range(size[1]):
        cells.append("")
        y += 1
        for x in range(size[0]):
            n = 0
            x = x+1
            for b in bomb_cords:
                b = (b[0]+1, b[1]+1)
                if  b[0] == x and b[1] == y:
                    n = "B"
                    break

                if abs(b[0]-x)+abs(b[1]-y) == 1:
                    n += 1
                elif abs(b[0]-x)==1 and abs(b[1]-y)==1:
                    n +=1

            cells[y-1] = cells[y-1] + str(n)

    return cells


def open_cell_for_cord(cord):
    for c in Cell_sprite:
        if c.pos() == cord:
            c.zero_check()

def cells_open(cord):
    global OPENNESS_MAP

    an_open = True
    while an_open:
        an_open = False
        for y, i in enumerate(CELLS_MAP):
            for x, j in enumerate(i):
                if abs(cord[0] - x) + abs(cord[1] - y) == 1:
                    OPENNESS_MAP[y] = OPENNESS_MAP[y][:x] + \
                                      "o" + OPENNESS_MAP[y][x + 1:]
                    an_open = True
                    open_cell_for_cord((x, y))
                elif abs(cord[0] - x) == 1 and abs(
                        cord[1] - y) == 1:
                    OPENNESS_MAP[y] = OPENNESS_MAP[y][:x] + \
                                      "o" + OPENNESS_MAP[y][x + 1:]

                    an_open = True
                    open_cell_for_cord((x, y))

        return an_open

def map_regenerate():
    global BOMB_COUNT, TIME_START
    Cell_sprite.update()
    Cell_sprite.draw(screen)
    pygame.display.flip()

    time.sleep(5)
    Cell_sprite.empty()
    load_map()
    global OPENNESS_MAP
    OPENNESS_MAP = ["c" * MAP_SIZE[0] for _ in range(MAP_SIZE[1])]

    BOMB_COUNT = BOMB
    TIME_START = time.time()

    caption_update()


class Cell(pygame.sprite.Sprite):
    def __init__(self, cord:(int, int), who:str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((CELL_SIZE-2, CELL_SIZE-2))
        self.image.fill("#A9A9A9")
        self.rect = self.image.get_rect()
        self.cord = cord
        self.rect.topleft = (self.cord[0]*CELL_SIZE+1,
                             self.cord[1]*CELL_SIZE+1)
        self.who = who
        self.open = False
        self.flag = False

    def update(self):
        if OPENNESS_MAP[self.cord[1]][self.cord[0]] == "o":
            self.open = True

        text = self.who
        if not self.open:
            text = ""

        self.font = pygame.font.SysFont("Arial", CELL_SIZE//3*2)
        self.textSurf = self.font.render(text, True,
                                 "#B22222" if self.who == "B" else "#006400")
        self.image = pygame.surface.Surface((CELL_SIZE-2, CELL_SIZE-2))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        if self.flag:
            self.image.fill("#FF5555")
        else:
            self.image.fill("#A9A9A9")
        self.image.blit(self.textSurf,
                        [CELL_SIZE / 2 - W / 2, CELL_SIZE / 2 - H / 2])


    def click(self):
        return self.rect

    def pos(self):
        return self.cord

    def zero_check(self):
        global OPENNESS_MAP

        if not self.open:
            if self.who == "0":
                self.open = True
                OPENNESS_MAP[self.cord[1]] = \
                    OPENNESS_MAP[self.cord[1]][:self.cord[0]] + \
                    "o" + OPENNESS_MAP[self.cord[1]][self.cord[0] + 1:]

                cells_open(self.cord)

    def open_action(self):
        global OPENNESS_MAP

        if not self.open:
            self.open = True
            OPENNESS_MAP[self.cord[1]] = \
                OPENNESS_MAP[self.cord[1]][:self.cord[0]] + \
                "o" + OPENNESS_MAP[self.cord[1]][self.cord[0]+1:]

        if self.who == "0":
            cells_open(self.cord)

        return self.who

    def flag_action(self):
        global BOMB_COUNT
        if self.flag:
            self.flag = False
            if self.who == "B":
                BOMB_COUNT += 1
                caption_update()
        else:
            self.flag = True
            if self.who == "B":
                BOMB_COUNT -= 1
                caption_update()

        if BOMB_COUNT == 0:
            pygame.display.set_caption("  !!!You win!!!  ")
            map_regenerate()


def load_map():
    global CELLS_MAP
    CELLS_MAP = map_generate(MAP_SIZE, BOMB)

    for y, i in enumerate(CELLS_MAP):
        for x, j in enumerate(i):
            cell = Cell(cord=(x, y), who=j)
            Cell_sprite.add(cell)

def click_handler(o_cell, button):

    if button == 1:
        cell_name = o_cell.open_action()

        if cell_name == "B":
            pygame.display.set_caption("  ups...  ")
            map_regenerate()

    elif button == 3:
        o_cell.flag_action()


Cell_sprite = pygame.sprite.Group()

load_map()

running_main_win = True
while running_main_win:
    clock.tick(FPS)
    caption_update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for cell in Cell_sprite:
                    if cell.click().collidepoint(event.pos):
                        click_handler(cell, 1)
            if event.button == 3:
                for cell in Cell_sprite:
                    if cell.click().collidepoint(event.pos):
                        click_handler(cell, 3)

    # обновление спрайтов
    Cell_sprite.update()

    # Отрисовка
    screen.fill(background_color)
    Cell_sprite.draw(screen)
    pygame.display.flip()
