import random
from collections import deque
from config import *
from cell import Cell

class Maze:
    def __init__(self):
        self.grid = [[Cell(c, r) for r in range(ROWS)] for c in range(COLS)]
        self._generate()

    def cell(self, c, r):
        return self.grid[c][r]

    def neighbours(self, c, r):
        result = []
        for d, (dc, dr) in DIRS.items():
            nc, nr = c + dc, r + dr
            if 0 <= nc < COLS and 0 <= nr < ROWS:
                result.append((d, self.grid[nc][nr]))
        return result

    def passable_neighbours(self, c, r):
        out = []
        for d, nb in self.neighbours(c, r):
            if not self.cell(c, r).walls[d]:
                out.append((nb.col, nb.row))
        return out

    def _generate(self):
        stack = []
        start = self.grid[0][0]
        start.visited = True
        stack.append(start)

        while stack:
            cur = stack[-1]
            options = [(d, n) for d, n in self.neighbours(cur.col, cur.row) if not n.visited]

            if options:
                d, nxt = random.choice(options)
                cur.walls[d] = False
                nxt.walls[OPPOSITE[d]] = False
                nxt.visited = True
                stack.append(nxt)
            else:
                stack.pop()

    def bfs_reachable(self, sc, sr, ec, er):
        q = deque([(sc, sr)])
        visited = {(sc, sr)}

        while q:
            c, r = q.popleft()
            for nc, nr in self.passable_neighbours(c, r):
                if (nc, nr) == (ec, er):
                    return True
                if (nc, nr) not in visited:
                    visited.add((nc, nr))
                    q.append((nc, nr))
        return False

    def quantum_collapse(self, player_pos, exit_pos):
        import random

        num_changes = random.randint(3, 5)
        changes = []

        for _ in range(num_changes):
            c = random.randint(0, COLS - 1)
            r = random.randint(0, ROWS - 1)
            d = random.choice(list(DIRS.keys()))

            nc, nr = c + DIRS[d][0], r + DIRS[d][1]
            if 0 <= nc < COLS and 0 <= nr < ROWS:
                a = self.grid[c][r]
                b = self.grid[nc][nr]

                a.walls[d] = not a.walls[d]
                b.walls[OPPOSITE[d]] = not b.walls[OPPOSITE[d]]
                changes.append((a, d, b, OPPOSITE[d]))

        if self.bfs_reachable(*player_pos, *exit_pos):
            return [(a, d) for a, d, _, _ in changes]
        else:
            for a, d, b, db in changes:
                a.walls[d] = not a.walls[d]
                b.walls[db] = not b.walls[db]
            return []

    def draw(self, pen):
        pen.clear()
        for col in self.grid:
            for cell in col:
                cell.draw(pen)

    def draw_flash(self, pen, changed):
        for cell, _ in changed:
            cell.draw(pen, flash=True)