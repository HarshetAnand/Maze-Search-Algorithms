# Maze Search Algorithms

A comparative study of uninformed and informed search algorithms applied to maze solving. Implements Breadth-First Search (BFS), Depth-First Search (DFS), and A* search with both Manhattan and Euclidean distance heuristics on a randomly generated 57x41 maze.

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

## Algorithms Implemented

**Uninformed Search:**
- **BFS:** Explores cells level by level, guarantees shortest path
- **DFS:** Explores deeply before backtracking, less memory but no shortest path guarantee

**Informed Search:**
- **A* with Manhattan distance:** Uses |dx| + |dy| as heuristic, optimal for grid movement
- **A* with Euclidean distance:** Uses √(dx² + dy²) as heuristic, more conservative estimate

## Output Files

The program generates multiple output files comparing the algorithms:
- Maze structure and successor matrix
- Action sequences for path reconstruction
- Visited cell maps for each algorithm
- Visual maze solution with path marked

## Key Concepts Demonstrated

- Graph search algorithms (BFS, DFS, A*)
- Heuristic design and admissibility
- Priority queue ordering with cost + heuristic
- Path reconstruction from parent pointers
- Algorithm complexity comparison
- Maze representation and parsing
