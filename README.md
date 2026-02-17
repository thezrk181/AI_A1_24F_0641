# AI Pathfinder – Uninformed Search in a Grid Environment

A Python GUI application that visualizes how six different **uninformed (blind) search algorithms** explore a 10×10 grid to find a path from **Start (S)** to **Target (T)**, while avoiding static walls.

## Algorithms Implemented

| # | Algorithm | Description |
|---|-----------|-------------|
| 1 | **BFS** (Breadth-First Search) | Explores level by level using a queue |
| 2 | **DFS** (Depth-First Search) | Explores as deep as possible using a stack |
| 3 | **UCS** (Uniform-Cost Search) | Expands the lowest-cost node first (accounts for diagonal cost √2) |
| 4 | **DLS** (Depth-Limited Search) | DFS with a configurable depth limit |
| 5 | **IDDFS** (Iterative Deepening DFS) | Repeats DLS with increasing depth limits |
| 6 | **Bidirectional Search** | Searches simultaneously from Start and Target until they meet |

## Features

- **Step-by-step visualization** with animated search progression
- **Frontier nodes** (light blue) – nodes waiting to be explored
- **Explored nodes** (dark blue) – nodes already visited
- **Final path** (purple) – shortest/found route highlighted
- **6-direction movement** (clockwise): Up, Right, Bottom, Bottom-Right, Left, Top-Left
- Configurable depth limit for DLS

## Requirements

- **Python 3.x**
- **Tkinter** (included with standard Python installation on most systems)

No additional packages need to be installed. Tkinter comes built-in with Python.

## How to Run

1. Clone or download this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-pathfinder.git
   cd ai-pathfinder
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. In the GUI:
   - Select an algorithm from the dropdown menu
   - (Optional) Set a depth limit if using DLS
   - Click **▶ Run Search** to visualize the pathfinding

## Grid Layout

- **Green (S)** – Start point at position (0, 0)
- **Red (T)** – Target point at position (9, 9)
- **Dark grey (■)** – Static walls/obstacles
- The grid is 10×10 with pre-defined wall placements

## Screenshots

*Run each algorithm to see the step-by-step visualization of frontier expansion, node exploration, and final path discovery.*

## Author

AI Assignment 1 – Uninformed Search Algorithms
