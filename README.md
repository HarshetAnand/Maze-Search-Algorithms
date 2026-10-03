# Maze Search Algorithms

A comparative study of uninformed and informed search algorithms applied to maze solving. Implements Breadth-First Search (BFS), Depth-First Search (DFS), and A* search with both Manhattan and Euclidean distance heuristics on an ASCII maze of any size.

## Features

- ASCII maze parsing and representation
- Cell-based graph structure with successor tracking
- Breadth-First Search (BFS) implementation
- Depth-First Search (DFS) implementation
- A* search with Manhattan distance heuristic
- A* search with Euclidean distance heuristic
- Path reconstruction and visualization
- Comparison of search efficiency across algorithms

## Tech Stack

- Python
- NumPy
- Math (standard library)

## Data

The script reads the maze from `maze.txt` in the project folder. The maze is drawn with `+`, `-`, and `|` characters, with each cell three characters wide and two characters tall:

    +--+--+--+
    |     |  |
    +  +--+  +
    |        |
    +--+--+--+

The entrance is the top-center cell and the exit is the bottom-center cell. The maze size is taken from the file, so any maze in this format works.

## Algorithms Implemented

**Uninformed Search:**

- **BFS:** Explores cells level by level, guarantees shortest path
- **DFS:** Explores deeply before backtracking, less memory but no shortest path guarantee

**Informed Search:**

- **A\* with Manhattan distance:** Uses |dx| + |dy| as heuristic, optimal for grid movement
- **A\* with Euclidean distance:** Uses √(dx² + dy²) as heuristic, more conservative estimate

## Output Files

- `successors.txt`: the moves available from each cell
- `solution_moves.txt`: the shortest path as a sequence of moves
- `solved_maze.txt`: the maze with the shortest path marked
- `bfs_visited.txt` and `dfs_visited.txt`: the cells each uninformed search visited
- `manhattan_distances.txt`: the Manhattan distance from each cell to the exit
- `astar_manhattan_visited.txt` and `astar_euclidean_visited.txt`: the cells A* visited under each heuristic

## Key Concepts Demonstrated

- Graph search algorithms (BFS, DFS, A*)
- Heuristic design and admissibility
- Priority queue ordering with cost + heuristic
- Path reconstruction from parent pointers
- Algorithm complexity comparison
- Maze representation and parsing
