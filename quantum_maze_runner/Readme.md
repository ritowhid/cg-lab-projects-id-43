# Quantum Maze Runner 🌀

A terminal-free, graphical maze game built with Python's `turtle` module. Navigate through a procedurally generated maze while being hunted by a ghost — and watch out, the maze itself randomly collapses and rebuilds around you!

---

## Features

- **Procedural maze generation** using recursive backtracking (DFS)
- **Quantum collapse mechanic** — walls randomly open and close every few seconds, keeping the maze in flux
- **Ghost AI** powered by A\* pathfinding that recalculates its route after every player move
- **Live HUD** showing collapse countdown and entity legend
- **Animated exit portal** that pulses between two colors
- **Game-over screen** with a live countdown before the next round begins automatically

---

## Project Structure

```
quantum_maze_runner/
│
├── main.py          # Entry point
├── game_engine.py   # Main game loop, rendering, HUD, and game-over logic
├── maze.py          # Maze generation, BFS reachability check, quantum collapse
├── cell.py          # Individual cell with wall state and drawing logic
├── player.py        # Player entity and movement
├── ghost.py         # Ghost entity with A* pathfinding
├── entity.py        # Base class for player and ghost (turtle rendering)
├── pathfinding.py   # A* algorithm
└── config.py        # All constants (grid size, colors, timing, etc.)
```

---

## Requirements

- Python 3.x (tested on 3.14)
- No third-party libraries — uses only the Python standard library (`turtle`, `heapq`, `collections`, `random`, `time`)

---

## How to Run

```bash
python main.py
```

Or with the full path:

```bash
python -u "path/to/quantum_maze_runner/main.py"
```

---

## Controls

| Key | Action |
|---|---|
| `W` or `↑` | Move North |
| `S` or `↓` | Move South |
| `A` or `←` | Move West |
| `D` or `→` | Move East |

---

## Gameplay

1. You start at the **top-left** corner of the maze.
2. The **EXIT** portal is at the **bottom-right** corner.
3. A **ghost** starts at the top-right and chases you using A\* pathfinding.
4. Every few seconds the maze **quantum collapses** — some walls toggle open or closed. The collapse is guaranteed never to cut off the path between you and the exit.
5. Reach the EXIT to win. Get caught by the ghost to lose.
6. After a game ends, a **10-second countdown** is shown before a new game starts automatically.

---

## Configuration

All game constants are in `config.py`. You can tweak them freely:

| Constant | Default | Description |
|---|---|---|
| `COLS`, `ROWS` | `15, 15` | Maze grid dimensions |
| `CELL_SIZE` | `36` | Pixel size of each cell |
| `COLLAPSE_INTERVAL` | `4.0` | Seconds between quantum collapses |
| `GHOST_MOVE_EVERY` | `2` | Ghost steps per player move |
| `WALL_WIDTH` | `2` | Thickness of maze walls |

Colors can also be changed in `config.py` — all values are standard hex color strings.

---

## How It Works

### Maze Generation
The maze is built using **recursive backtracking**: starting from cell (0, 0), the algorithm randomly carves passages to unvisited neighbours until every cell has been visited, producing a perfect maze with exactly one path between any two cells.

### Quantum Collapse
Every `COLLAPSE_INTERVAL` seconds, 3–5 random walls are toggled. After toggling, a **BFS reachability check** verifies that the player can still reach the exit. If not, all changes are rolled back, keeping the game always winnable.

### Ghost AI
After every player move, the ghost runs **A\*** from its current position to the player's position, then takes one step along that path. This gives the ghost perfect knowledge but still makes it beatable.

---

## License

© 2026 — All rights reserved. This project is for personal use only. Do not copy, distribute, or reuse without permission.