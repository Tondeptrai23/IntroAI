# Intro To AI Pacman

## Overview

This project was developed as part of the CSC14003 Intro To AI course at HCMUS.

### About the layout

The layout of the game is represented as a grid, where each cell can be one of the following:

- `.`: A food pellet
- `1`, `2`, `3`, `4`: Spawn points for the ghosts
- `P`: Pacman
- `#`: A wall
- ` `: An empty space

If you want to add a new layout, you can create a new file in the `layouts` folder with the same format as the existing layouts.

### Warning

Make sure that the layout is valid. If you are running 1 agent, only 1 spawn point should be appeared and so on.

## Run the Project

To run the project, you need to have Python 3 installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Game

```bash
python pacman.py -l <layout> -z <zoom_level> <args>
```

- `layout`: The layout of the game. You can choose from the available layouts in the `layouts` folder.
- `zoom_level`: The zoom level of the game. You can choose from 0.5, 1, 2, or 3.
- `--expand`: See the expansion of the ghost.

### Run a specific agent

Edit the `pacman.py` at line 650-654 (uncomment needed agent). You can choose from the following agents:

- `DFSGhost(index)`: A ghost that uses depth-first search to find the shortest path to Pacman.
- `BFSGhost(index)`: A ghost that uses breadth-first search to find the shortest path to Pacman.
- `AStarGhost(index)`: A ghost that uses A\* search to find the shortest path to Pacman.
- `UCSGhost(index)`: A ghost that uses UCS to find the shortest path to Pacman.

## Attribution

This project is based on the the Pacman AI projects developed at UC Berkeley with some modifications.

- The original Pacman AI projects were created by John DeNero and Dan Klein.
- More info at: http://ai.berkeley.edu/search.html

This project is used `only for educational purposes` in accordance with the licensing terms:

- No solutions from the original projects are included or distributed.
- This notice and attribution are retained.
