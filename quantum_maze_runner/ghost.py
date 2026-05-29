from entity import Entity
from config import *
from pathfinding import astar

class Ghost(Entity):
    def __init__(self, col, row):
        super().__init__(col, row, GHOST_COLOR)
        self.path = []
        self.index = 0

    def recalc(self, maze, goal):
        self.path = astar(maze, self.pos, goal)
        self.index = 0

    def step(self, maze):
        if not self.path:
            return
        if self.index + 1 < len(self.path):
            self.index += 1
            self.col, self.row = self.path[self.index]
            self.teleport(maze)