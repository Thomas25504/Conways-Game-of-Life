# Conways-Game-of-Life
 A visual representation of conway's game of life made in python

 Conway's Game of Life is a zero-player game created by mathematician John Conway in 1970. It's a fascinating simulation that models cellular automation — a grid of cells that evolve over time based on simple rules.

### Concept
The game is played on a 2D grid where each cell can be in one of two states:
🟩 Alive (1)
⬛ Dead (0)

Each cell interacts with its eight immediate neighbors (horizontal, vertical, and diagonal).

### Rules of the Game
Each cell's fate is determined by these four simple rules:

Underpopulation:
🔺 Any alive cell with fewer than 2 live neighbors dies (loneliness).

Survival:
🔹 Any alive cell with 2 or 3 live neighbors continues to live.

Overpopulation:
🔻 Any alive cell with more than 3 live neighbors dies (overcrowding).

Reproduction:
🌱 Any dead cell with exactly 3 live neighbors becomes alive (birth).
