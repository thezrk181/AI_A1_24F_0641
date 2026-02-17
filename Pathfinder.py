import tkinter as tk
import time
import random
from collections import deque
import heapq

# ──────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────
ROWS           = 10
COLS           = 10
CELL_SIZE      = 54
STEP_DELAY     = 0.18   # seconds between animation frames

# Diagonal move cost (√2) for UCS
DIAG_COST = 1.414

# ──────────────────────────────────────────
#  COLORS
# ──────────────────────────────────────────
COLOR = {
    "empty"        : "#F5F5F5",
    "wall"         : "#2C2C2C",
    "start"        : "#27AE60",
    "target"       : "#E74C3C",
    "frontier"     : "#AED6F1",
    "explored"     : "#2980B9",
    "path"         : "#8E44AD",
    # Bidirectional-specific
    "fwd_frontier" : "#AED6F1",
    "bwd_frontier" : "#FADBD8",
    "fwd_explored" : "#2980B9",
    "bwd_explored" : "#C0392B",
    "meet"         : "#F39C12",
}

# ──────────────────────────────────────────
#  STATIC GRID  (0 = empty, 1 = wall)
# ──────────────────────────────────────────
BASE_GRID = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,0,1,0,0,0,0,1,0,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]

START  = (0, 0)
TARGET = (9, 9)

# Live grid (reset before each run)
grid = [row[:] for row in BASE_GRID]

# ──────────────────────────────────────────
#  MOVEMENT ORDER  (6 directions – black text)
#  Up, Right, Bottom, Bottom-Right, Left, Top-Left
# ──────────────────────────────────────────
DIRECTIONS = [
    (-1,  0),   # Up
    ( 0,  1),   # Right
    ( 1,  0),   # Bottom
    ( 1,  1),   # Bottom-Right (diagonal)
    ( 0, -1),   # Left
    (-1, -1),   # Top-Left (diagonal)
]

DIAG_PAIRS = {(1, 1), (-1, -1)}


# ──────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────

def reset_grid():
    """Restore grid to static walls only."""
    global grid
    grid = [row[:] for row in BASE_GRID]


def get_neighbors(row, col):
    """Yield valid (r, c, cost) neighbours in the required direction order."""
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == 0:
            cost = DIAG_COST if (dr, dc) in DIAG_PAIRS else 1.0
            yield r, c, cost
