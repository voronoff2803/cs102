import pygame
from pygame.locals import *
import random
import copy
from copy import deepcopy


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=30):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Thrones')
        self.screen.fill(pygame.Color('white'))
        running = True
        self.clist = self.cell_list(randomize=True)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(self.clist)
            self.update_cell_list(self.clist)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=False):
        if randomize:
            clist = [[random.randint(0, 1) for y in range(self.cell_width)] for x in range(self.cell_height)]
        else:
            clist = [[0 for y in range(self.cell_width)] for x in range(self.cell_height)]
        return clist

    def draw_cell_list(self, rects):
        for i in range(len(rects)):
            for j in range(len(rects[i])):
                if rects[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('gray'), (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size))
                elif rects[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size))

    def get_neighbours(self, cell):
        return [self.clist[i + cell[0]][j + cell[1]] for i in range(-1, 2) for j in range(-1, 2) if (i | j) and
                      0 <= cell[0] + i < self.cell_height and 0 <= cell[1] + j < self.cell_width]

    def update_cell_list(self, cell_list):
        new_list = deepcopy(cell_list)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if cell_list[i][j]:
                    if sum(self.get_neighbours((i, j))) in (2, 3):
                        new_list[i][j] = 1
                    else:
                        new_list[i][j] = 0
                else:
                    if sum(self.get_neighbours((i, j))) == 3:
                        new_list[i][j] = 1
                    else:
                        new_list[i][j] = 0
        self.clist = new_list
        return new_list


if __name__ == '__main__':
    game = GameOfLife(600, 600, 10)
    game.run()
