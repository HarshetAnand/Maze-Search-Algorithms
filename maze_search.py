"""Solve an ASCII maze with four search strategies and compare them.

The maze is read from a text file drawn with '+', '-' and '|' characters.
Each cell is three characters wide and two characters tall, for example:

    +--+--+--+
    |     |  |
    +  +--+  +
    |        |
    +--+--+--+

The entrance is the top-center cell and the exit is the bottom-center cell.

The script runs breadth-first search, depth-first search, and A* search with
two heuristics (Manhattan and Euclidean distance to the exit). It writes the
shortest path, the solved maze, and the set of cells each strategy visited,
so the strategies can be compared by how much of the maze they explore.
"""

import math

import numpy as np

MAZE_FILE = 'maze.txt'

# Codes used in the character grid.
SPACE, CORNER, HORIZONTAL_WALL, VERTICAL_WALL, PATH = 0, 1, 2, 3, 4


# ---------------------------------------------------------------------------
# Maze loading
# ---------------------------------------------------------------------------

with open(MAZE_FILE, 'r') as file:
    data = [row.strip() for row in file if row.strip()]

# Maze size in cells, taken from the size of the drawing.
height = (len(data) - 1) // 2
width = (len(data[0]) - 1) // 3
center_idx = int((width - 1) / 2)

start = (0, center_idx)
goal = (height - 1, center_idx)

# Character grid as numbers, used later to draw the solution.
M = np.zeros([height * 2 + 1, width * 3 + 1])
for h in range(height * 2 + 1):
    for w in range(width * 3 + 1):
        if data[h][w] == ' ':
            M[h, w] = SPACE
        if data[h][w] == '+':
            M[h, w] = CORNER
        if data[h][w] == '-':
            M[h, w] = HORIZONTAL_WALL
        if data[h][w] == '|':
            M[h, w] = VERTICAL_WALL


class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.succ = ''    # moves available from this cell, a subset of 'UDLR'
        self.action = ''  # the move the parent took to reach this cell


cells = [[Cell(i, j) for j in range(width)] for i in range(height)]

# A move is available when there is no wall on that side of the cell.
succ_matrix = []
for i in range(1, len(data), 2):
    curr_row = []
    for j in range(1, len(data[0]) - 1, 3):
        curr_cell = ''
        if data[i - 1][j] == ' ':
            if i != 1:  # the entrance is open, but do not leave the maze
                curr_cell += 'U'
        if data[i + 1][j] == ' ':
            if i != len(data) - 2:  # the exit is open, but do not leave the maze
                curr_cell += 'D'
        if data[i][j - 1] == ' ':
            curr_cell += 'L'
        if data[i][j + 2] == ' ':
            curr_cell += 'R'
        curr_row.append(curr_cell)
    succ_matrix.append(curr_row)

for i in range(height):
    for j in range(width):
        cells[i][j].succ = succ_matrix[i][j]


def write_visited(filename, visited):
    """Write a grid of 1s and 0s marking which cells a search visited."""
    with open(filename, "w") as f:
        for h in range(height):
            for w in range(width):
                f.write("1" if (h, w) in visited else "0")
                if w != width - 1:
                    f.write(",")
            f.write("\n")


with open("successors.txt", "w") as f:
    for cell_row in cells:
        f.write(",".join([cell_col.succ for cell_col in cell_row]) + "\n")


# ---------------------------------------------------------------------------
# Breadth-first search
# ---------------------------------------------------------------------------

# Expand the maze one layer at a time. s1 is the current layer and s2 collects
# the next one. Each cell records the move that first reached it, which is
# enough to rebuild the shortest path afterward.
visited = set()
s1 = {start}
s2 = set()
while goal not in visited:
    for a in s1:
        visited.add(a)
        i, j = a[0], a[1]
        succ = cells[i][j].succ
        if 'U' in succ and (i - 1, j) not in (s1 | s2 | visited):
            s2.add((i - 1, j))
            cells[i - 1][j].action = 'U'
        if 'D' in succ and (i + 1, j) not in (s1 | s2 | visited):
            s2.add((i + 1, j))
            cells[i + 1][j].action = 'D'
        if 'L' in succ and (i, j - 1) not in (s1 | s2 | visited):
            s2.add((i, j - 1))
            cells[i][j - 1].action = 'L'
        if 'R' in succ and (i, j + 1) not in (s1 | s2 | visited):
            s2.add((i, j + 1))
            cells[i][j + 1].action = 'R'

    s1 = s2
    s2 = set()

write_visited("bfs_visited.txt", visited)


# ---------------------------------------------------------------------------
# Shortest path
# ---------------------------------------------------------------------------

# Walk backward from the exit, undoing the recorded move at each cell.
cur = goal
s = ''
seq = []

while cur != start:
    seq.append(cur)
    i, j = cur[0], cur[1]
    t = cells[i][j].action
    s += t

    if t == 'U': cur = (i + 1, j)
    if t == 'D': cur = (i - 1, j)
    if t == 'L': cur = (i, j + 1)
    if t == 'R': cur = (i, j - 1)

action = s[::-1]

with open("solution_moves.txt", "w") as f:
    f.write(action + "\n")

seq.append(start)
seq = seq[::-1]

# Mark the path on the character grid, including the gaps between cells.
for (a, b) in seq:
    M[2 * a + 1, 3 * b + 1] = PATH
    M[2 * a + 1, 3 * b + 2] = PATH
    if (a + 1, b) in seq and M[2 * a + 2, 3 * b + 1] != HORIZONTAL_WALL:
        M[2 * a + 2, 3 * b + 1] = PATH
        M[2 * a + 2, 3 * b + 2] = PATH

    if (a, b - 1) in seq and M[2 * a + 1, 3 * b] != CORNER and M[2 * a + 1, 3 * b] != VERTICAL_WALL:
        M[2 * a + 1, 3 * b] = PATH

# Mark the entrance and exit openings.
M[0, 3 * center_idx + 1] = PATH
M[0, 3 * center_idx + 2] = PATH
M[2 * height, 3 * center_idx + 1] = PATH
M[2 * height, 3 * center_idx + 2] = PATH

symbols = {SPACE: ' ', CORNER: '+', HORIZONTAL_WALL: '-', VERTICAL_WALL: '|', PATH: '@'}

with open("solved_maze.txt", "w") as f:
    for h in range(height * 2 + 1):
        for w in range(width * 3 + 1):
            f.write(symbols[M[h, w]])
        f.write('\n')


# ---------------------------------------------------------------------------
# Depth-first search
# ---------------------------------------------------------------------------

# Follow one branch as far as it goes before backing up. The most recently
# discovered cell is always expanded next, so the frontier is a stack.
visited = set()
stack = [start]

while stack and goal not in visited:
    a = stack.pop()
    if a in visited:
        continue
    visited.add(a)

    i, j = a[0], a[1]
    succ = cells[i][j].succ
    if 'U' in succ and (i - 1, j) not in visited:
        stack.append((i - 1, j))
    if 'D' in succ and (i + 1, j) not in visited:
        stack.append((i + 1, j))
    if 'L' in succ and (i, j - 1) not in visited:
        stack.append((i, j - 1))
    if 'R' in succ and (i, j + 1) not in visited:
        stack.append((i, j + 1))

write_visited("dfs_visited.txt", visited)


# ---------------------------------------------------------------------------
# A* search
# ---------------------------------------------------------------------------

# Two estimates of the remaining distance from each cell to the exit.
man = {(i, j): abs(i - (height - 1)) + abs(j - center_idx)
       for j in range(width) for i in range(height)}
euc = {(i, j): math.sqrt((i - (height - 1)) ** 2 + (j - center_idx) ** 2)
       for j in range(width) for i in range(height)}

with open("manhattan_distances.txt", "w") as f:
    for h in range(height):
        for w in range(width):
            f.write(str(man[(h, w)]))
            if w != width - 1:
                f.write(",")
        f.write("\n")


def a_star_search(height, width, dist_method, man, euc):
    """Run A* from the entrance to the exit and return the cells it visited.

    Cells are expanded in order of g + h, where g is the number of moves taken
    so far and h is the chosen heuristic. dist_method should be either
    'manhattan' or 'euclidean'.
    """
    if dist_method == 'manhattan':
        heuristic = man
    elif dist_method == 'euclidean':
        heuristic = euc
    else:
        raise ValueError('distance method should be either manhattan or euclidean')

    g = {(i, j): float('inf') for j in range(width) for i in range(height)}
    g[(0, center_idx)] = 0

    queue = [(0, center_idx)]
    visited = set()

    while queue and (height - 1, center_idx) not in visited:
        queue.sort(key=lambda x: g[x] + heuristic[x])
        point = queue.pop(0)
        if point not in visited:
            visited.add(point)
            i, j = point[0], point[1]
            succ = cells[i][j].succ
            if 'U' in succ and (i - 1, j) not in visited:
                if (i - 1, j) not in queue: queue += [(i - 1, j)]
                g[(i - 1, j)] = min(g[(i - 1, j)], g[(i, j)] + 1)
            if 'D' in succ and (i + 1, j) not in visited:
                if (i + 1, j) not in queue: queue += [(i + 1, j)]
                g[(i + 1, j)] = min(g[(i + 1, j)], g[(i, j)] + 1)
            if 'L' in succ and (i, j - 1) not in visited:
                if (i, j - 1) not in queue: queue += [(i, j - 1)]
                g[(i, j - 1)] = min(g[(i, j - 1)], g[(i, j)] + 1)
            if 'R' in succ and (i, j + 1) not in visited:
                if (i, j + 1) not in queue: queue += [(i, j + 1)]
                g[(i, j + 1)] = min(g[(i, j + 1)], g[(i, j)] + 1)
    return visited


a_star_man_visited = a_star_search(height, width, 'manhattan', man, euc)
a_star_euclidean_visited = a_star_search(height, width, 'euclidean', man, euc)

write_visited("astar_manhattan_visited.txt", a_star_man_visited)
write_visited("astar_euclidean_visited.txt", a_star_euclidean_visited)
