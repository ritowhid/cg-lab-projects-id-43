CELL_SIZE = 36
COLS, ROWS = 15, 15
MARGIN_TOP = 60

COLLAPSE_INTERVAL = 4.0
GHOST_MOVE_EVERY = 2
WALL_WIDTH = 2

WIN_W = COLS * CELL_SIZE + 40
WIN_H = ROWS * CELL_SIZE + MARGIN_TOP + 40

# Directions — N is row-1 (up on screen), S is row+1 (down on screen)
DIRS = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
}
OPPOSITE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

# Colors
BG_COLOR = "#0a0a0f"
WALL_COLOR = "#00ff88"
WALL_FLASH = "#ffffff"
PLAYER_COLOR = "#ffff00"
GHOST_COLOR = "#ff2244"
EXIT_COLOR_A = "#0044ff"
EXIT_COLOR_B = "#00aaff"
HUD_COLOR = "#00ffcc"
TEXT_COLOR = "#ccffee"