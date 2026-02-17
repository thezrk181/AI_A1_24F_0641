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


# ──────────────────────────────────────────
#  DRAWING – standard
# ──────────────────────────────────────────

def draw_grid(canvas, frontier=frozenset(), explored=frozenset(),
              path=frozenset(), status=""):
    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = col * CELL_SIZE, row * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            cell = (row, col)

            if cell == START:
                color = COLOR["start"]
            elif cell == TARGET:
                color = COLOR["target"]
            elif grid[row][col] == 1:
                color = COLOR["wall"]
            elif cell in path:
                color = COLOR["path"]
            elif cell in explored:
                color = COLOR["explored"]
            elif cell in frontier:
                color = COLOR["frontier"]
            else:
                color = COLOR["empty"]

            canvas.create_rectangle(x1, y1, x2, y2,
                                    fill=color, outline="#BBBBBB", width=1)

            if cell == START:
                label, fg = "S", "white"
            elif cell == TARGET:
                label, fg = "T", "white"
            elif grid[row][col] == 1:
                label, fg = "■", "#AAAAAA"
            else:
                label, fg = "", "black"

            if label:
                canvas.create_text(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2,
                                   text=label, fill=fg,
                                   font=("Arial", 14, "bold"))

    canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE + 15,
                       text=status, fill="#333333",
                       font=("Arial", 10, "italic"))


# ──────────────────────────────────────────
#  DRAWING – Bidirectional variant
# ──────────────────────────────────────────

def draw_grid_bidir(canvas,
                    fwd_frontier=frozenset(), bwd_frontier=frozenset(),
                    fwd_explored=frozenset(), bwd_explored=frozenset(),
                    path=frozenset(), meet=None, status=""):
    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = col * CELL_SIZE, row * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            cell = (row, col)

            if cell == START:
                color = COLOR["start"]
            elif cell == TARGET:
                color = COLOR["target"]
            elif grid[row][col] == 1:
                color = COLOR["wall"]
            elif cell in path:
                color = COLOR["path"]
            elif cell == meet:
                color = COLOR["meet"]
            elif cell in fwd_explored and cell in bwd_explored:
                color = COLOR["meet"]
            elif cell in fwd_explored:
                color = COLOR["fwd_explored"]
            elif cell in bwd_explored:
                color = COLOR["bwd_explored"]
            elif cell in fwd_frontier:
                color = COLOR["fwd_frontier"]
            elif cell in bwd_frontier:
                color = COLOR["bwd_frontier"]
            else:
                color = COLOR["empty"]

            canvas.create_rectangle(x1, y1, x2, y2,
                                    fill=color, outline="#BBBBBB", width=1)

            if cell == START:
                label, fg = "S", "white"
            elif cell == TARGET:
                label, fg = "T", "white"
            elif grid[row][col] == 1:
                label, fg = "■", "#AAAAAA"
            else:
                label, fg = "", "black"

            if label:
                canvas.create_text(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2,
                                   text=label, fill=fg,
                                   font=("Arial", 14, "bold"))

    canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE + 15,
                       text=status, fill="#333333",
                       font=("Arial", 10, "italic"))


# ──────────────────────────────────────────
#  RUN BUTTON CALLBACK (placeholder – no algorithms yet)
# ──────────────────────────────────────────

def run_algorithm():
    reset_grid()
    draw_grid(canvas, status="No algorithms implemented yet…")
    canvas.update()


# ──────────────────────────────────────────
#  LEGEND
# ──────────────────────────────────────────

def build_legend(parent):
    frame = tk.Frame(parent, bg="#FAFAFA", bd=1, relief=tk.GROOVE)
    frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    items = [
        (COLOR["start"],        "Start (S)"),
        (COLOR["target"],       "Target (T)"),
        (COLOR["wall"],         "Static Wall"),
        (COLOR["fwd_frontier"], "Fwd Frontier"),
        (COLOR["bwd_frontier"], "Bwd Frontier"),
        (COLOR["fwd_explored"], "Fwd Explored"),
        (COLOR["bwd_explored"], "Bwd Explored"),
        (COLOR["meet"],         "Meeting Node"),
        (COLOR["path"],         "Final Path"),
    ]

    for i, (color, label) in enumerate(items):
        tk.Label(frame, bg=color, width=2,
                 relief=tk.RAISED).grid(row=0, column=i*2,   padx=(6, 2), pady=5)
        tk.Label(frame, text=label, bg="#FAFAFA",
                 font=("Arial", 8)).grid(row=0, column=i*2+1, padx=(0, 8))


# ──────────────────────────────────────────
#  MAIN WINDOW
# ──────────────────────────────────────────

root = tk.Tk()
root.title("AI Pathfinder – BFS / DFS / UCS / DLS / IDDFS / Bidir")
root.resizable(False, False)
root.configure(bg="#FAFAFA")

# Title label inside window
tk.Label(root, text="AI Pathfinder – Uninformed Search",
         font=("Arial", 15, "bold"), bg="#FAFAFA").pack(pady=(10, 2))

tk.Label(root,
         text="Visualizing search step-by-step on a static grid",
         font=("Arial", 9, "italic"), fg="#888888", bg="#FAFAFA").pack(pady=(0, 6))

# Canvas  (extra 30 px for status bar)
canvas = tk.Canvas(root,
                   width=COLS * CELL_SIZE,
                   height=ROWS * CELL_SIZE + 30,
                   bg="#FAFAFA", bd=0, highlightthickness=0)
canvas.pack(padx=10)

# Controls row
ctrl = tk.Frame(root, bg="#FAFAFA")
ctrl.pack(pady=8)

tk.Label(ctrl, text="Algorithm:", bg="#FAFAFA",
         font=("Arial", 11)).grid(row=0, column=0, padx=6)

algo_var = tk.StringVar(root)
algo_var.set("BFS")
tk.OptionMenu(ctrl, algo_var, "BFS", "DFS").grid(row=0, column=1, padx=6)

run_btn = tk.Button(ctrl, text="▶  Run Search",
                    command=run_algorithm,
                    bg="#2980B9", fg="white",
                    font=("Arial", 11, "bold"),
                    relief=tk.FLAT, padx=12, pady=4)
run_btn.grid(row=0, column=2, padx=10)

# Legend
build_legend(root)

# Initial draw
draw_grid(canvas, status="Select an algorithm and press ▶ Run Search")

root.mainloop()
