import turtle
from config import *

class Cell:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False

    def pixel_origin(self):
        x = self.col * CELL_SIZE - (COLS * CELL_SIZE) / 2
        y = -self.row * CELL_SIZE + (ROWS * CELL_SIZE) / 2 - MARGIN_TOP / 2
        return x, y

    def center(self):
        x, y = self.pixel_origin()
        return x + CELL_SIZE / 2, y - CELL_SIZE / 2

    def draw(self, pen, flash=False):
        ox, oy = self.pixel_origin()
        color = WALL_FLASH if flash else WALL_COLOR
        pen.color(color)
        pen.width(WALL_WIDTH)

        segments = []
        # N wall = top edge (oy), S wall = bottom edge (oy - CELL_SIZE)
        if self.walls['N']:
            segments.append(((ox, oy), (ox + CELL_SIZE, oy)))
        if self.walls['S']:
            segments.append(((ox, oy - CELL_SIZE), (ox + CELL_SIZE, oy - CELL_SIZE)))
        if self.walls['W']:
            segments.append(((ox, oy), (ox, oy - CELL_SIZE)))
        if self.walls['E']:
            segments.append(((ox + CELL_SIZE, oy), (ox + CELL_SIZE, oy - CELL_SIZE)))

        for (x1, y1), (x2, y2) in segments:
            pen.penup()
            pen.goto(x1, y1)
            pen.pendown()
            pen.goto(x2, y2)