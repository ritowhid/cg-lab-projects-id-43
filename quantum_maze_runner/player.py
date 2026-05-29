from entity import Entity
from config import *

class Player(Entity):
    def __init__(self, col, row):
        super().__init__(col, row, PLAYER_COLOR)

    def try_move(self, maze, direction):
        cell = maze.cell(self.col, self.row)
        if cell.walls.get(direction, True):
            return False

        dc, dr = DIRS[direction]
        self.col += dc
        self.row += dr
        self.teleport(maze)
        return True