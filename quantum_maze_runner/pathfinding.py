import heapq

def astar(maze, start, goal):
    if start == goal:
        return [start]

    def h(p):
        return abs(p[0]-goal[0]) + abs(p[1]-goal[1])

    open_set = [(0, start)]
    came = {start: None}
    g = {start: 0}

    while open_set:
        _, cur = heapq.heappop(open_set)

        if cur == goal:
            path = []
            while cur:
                path.append(cur)
                cur = came[cur]
            return path[::-1]

        for nb in maze.passable_neighbours(*cur):
            cost = g[cur] + 1
            if nb not in g or cost < g[nb]:
                g[nb] = cost
                came[nb] = cur
                heapq.heappush(open_set, (cost + h(nb), nb))

    return []