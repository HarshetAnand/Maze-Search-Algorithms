import numpy as np
import math

# modify weight and height by yourself
# the width I had was 57 while the height I had was 41
width, height = 57, 41
center_idx = int((width-1)/2)

M = np.zeros([height*2+1, width*3+1]) # space

# example-maze is the example maze shown to you. You can copy and past
# the content in the example maze into a txt file and name it `example-maze.txt`
file = open('example-maze.txt', 'r')
data = []
for row in file:
    data.append(row.strip())

# Iterate through each cell of the 'data' list and convert the ASCII characters to numeric values in the 'M' array.
for h in range(height*2+1):
    for w in range(width*3+1):
        if data[h][w] == ' ':
            M[h,w] = 0 # 0 for ' '
        if data[h][w] == '+':
            M[h,w] = 1 # 1 for "+"
        if data[h][w] == '-':
            M[h,w] = 2 # 2 for '-'
        if data[h][w] == '|':
            M[h,w] = 3 # 3 for '|'
            # Uncomment the following lines to print the resulting 'M' array and its shape.
# print(M)
# print(M.shape)

# Define the 'Cell' class to represent each cell in the grid.
class Cell:
    def _init_(self, i, j):
        # Constructor method to initialize the cell with its row 'i' and column 'j' coordinates.
        self.i = i
        self.j = j
        self.succ = ''
        self.action = ''  # which action the parent takes to get this cell

        # Create a 2D list 'cells' to represent the grid of 'Cell' objects.
        # Each element in 'cells' will be a 'Cell' object initialized with its corresponding row and column index.
cells = [[Cell(i,j) for j in range(width)] for i in range(height)]

# Initialize an empty list 'succ_matrix' to store the successor directions for each cell in the maze.
succ_matrix = []
# Iterate through each row in the 'data' list (maze representation).
for i in range(1,len(data),2):
    curr_row = []
    # Iterate through each column in the current row.
    for j in range(1,len(data[0])-1,3):
        curr_cell = ''

        # Check for available successors (adjacent cells with space) and add them to 'curr_cell'.
        if data[i-1][j] == ' ':
            if i != 1: # prevent leaving the maze
                curr_cell += 'U'
        if data[i+1][j] == ' ':
            if i != len(data)-2: # prevent leaving the maze
                curr_cell += 'D'
        if data[i][j-1] == ' ':
            curr_cell += 'L'
        if data[i][j+2] == ' ':
            curr_cell += 'R'
        curr_row.append(curr_cell)
    succ_matrix.append(curr_row)

# Update the 'succ' attribute of each cell in the 'cells' array using the 'succ_matrix'.
for i in range(height):
    for j in range(width):
        cells[i][j].succ = succ_matrix[i][j]

# Save the successor matrix to a file named "Question2.txt" in a CSV format.
with open("Question2.txt", "w") as f:
    for cell_row in cells:
        # Write the comma-separated successor directions for each cell in the current row to the file.
        f.write(",".join([cell_col.succ for cell_col in cell_row]) + "\n")


# Initialize an empty set 'visited' to keep track of visited cells during the BFS.
visited = set()
# entrance:
s1 = {(0,center_idx)}
s2 = set()
while (height - 1, center_idx) not in visited:
    for a in s1:
        visited.add(a)
        i, j = a[0], a[1]
        succ = cells[i][j].succ
        if 'U' in succ and (i-1,j) not in (s1 | s2 | visited):
            s2.add((i-1,j))
            cells[i-1][j].action = 'U'
        if 'D' in succ and (i+1,j) not in (s1 | s2 | visited):
            s2.add((i+1,j))
            cells[i+1][j].action = 'D'
        if 'L' in succ and (i,j-1) not in (s1 | s2 | visited):
            s2.add((i,j-1))
            cells[i][j-1].action = 'L'
        if 'R' in succ and (i,j+1) not in (s1 | s2 | visited):
            s2.add((i,j+1))
            cells[i][j+1].action = 'R'

 # Update 's1' with the cells to explore in the next iteration, and reset 's2' for the next iteration.
    s1 = s2
    s2 = set()

# The following lines of code are for BFS
# Save the visited cells from the DFS algorithm to a file "Question5.txt" in a CSV format.
with open("Question5.txt", "w") as f:
    for h in range(height):
        for w in range(width):
            # Write "1" to the file if the cell (h, w) is visited; otherwise, write "0".
            f.write("1" if (h, w) in visited else "0")
            if w != width - 1:
                f.write(",")
        f.write("\n")

# Initialize the current cell 'cur' to the goal cell (height - 1, center_idx).
cur = (height - 1, center_idx)
s = ''
seq = []

# While the current cell is not the starting cell (0, center_idx), record the actions and update the 'cur' cell.
while cur != (0, center_idx):
    seq.append(cur)
    i, j = cur[0], cur[1]
    t = cells[i][j].action
    s += t

    # Update the 'cur' cell based on the action taken.
    if t == 'U': cur = (i+1, j)
    if t == 'D': cur = (i-1, j)
    if t == 'L': cur = (i, j+1)
    if t == 'R': cur = (i, j-1)

    # Reverse the sequence of actions to get the correct order.
action = s[::-1]

# Write the action sequence to a file named "Question3.txt".
with open("Question3.txt", "w") as f:
    f.write(action + "\n")

# Add the starting and goal cells to the 'seq' list.
seq.append((0, center_idx))
seq = seq[::-1]

# Update the maze grid 'M' to mark the cells that form the path with the value 4.
for (a,b) in seq:
    M[2*a+1, 3*b+1] = 4
    M[2*a+1, 3*b+2] = 4
    if (a+1,b) in seq and M[2*a+2, 3*b+1] != 2:
        M[2*a+2, 3*b+1] = 4
        M[2*a+2, 3*b+2] = 4

    if (a,b-1) in seq and M[2*a+1, 3*b] != 1 and M[2*a+1, 3*b] != 3:
        M[2*a+1, 3*b] = 4

# Mark the starting and goal cells in 'M' with the value 4.
M[0,3*center_idx+1] = 4
M[0,3*center_idx+2] = 4
M[2*height,3*center_idx+1] = 4
M[2*height,3*center_idx+2] = 4

# The following lines of code are for the Maze
# Save the maze solution to a file "Question4.txt" with a visual representation using ASCII characters.
with open("Question4.txt", "w") as f:
    for h in range(height*2+1):
        for w in range(width*3+1):
            # Determine the appropriate ASCII character based on the value of M[h, w].
            if M[h,w]==0:
                f.write(' ')
            elif M[h,w]==1:
                f.write('+')
            elif M[h,w]==2:
                f.write('-')
            elif M[h,w]==3:
                f.write('|')
            elif M[h,w]==4:
                f.write('@')
                # Move to the next line after each row is written.
        f.write('\n')


# The following code performs depth first search.
# We start off with initializing an empty set to store the visited cells during the DFS traversal.
visited = set()
s1 = [(0, center_idx)]
s2 = set()

# Perform the DFS traversal while the goal cell (height-1, center_idx) has not been visited.
while (height-1, center_idx) not in visited:
    # Explore the cells in the current iteration (stack 's1').
    for a in s1:
        visited.add(a)

        # Extract the row 'i' and column 'j' from the current cell.
        i, j = a[0], a[1]
        succ = cells[i][j].succ

        # Check and add neighboring cells to 's2' if they are valid and not yet explored.
        # Also, record the action to reach the neighbor cell.
        if 'U' in succ and (i - 1, j) not in (s2 | visited) and (i - 1, j) not in s1:
            s2.add((i - 1, j))
            cells[i - 1][j].action = 'U'
        if 'D' in succ and (i + 1, j) not in (s2 | visited) and (i + 1, j) not in s1:
            s2.add((i + 1, j))
            cells[i + 1][j].action = 'D'
        if 'L' in succ and (i, j - 1) not in (s2 | visited) and (i, j - 1) not in s1:
            s2.add((i, j - 1))
            cells[i][j - 1].action = 'L'
        if 'R' in succ and (i, j + 1) not in (s2 | visited) and (i, j + 1) not in s1:
            s2.add((i, j + 1))
            cells[i][j + 1].action = 'R'
        # Transfer the cells from 's2' to 's1' for the next iteration.
    for b in s2:
        s1.append(b)

    # Reverse the order of cells in 's1' to ensure DFS exploration.
    s1.reverse()
    # Clear 's2' for the next iteration.
    s2 = set()

# Save the visited squares from the Depth-First Search (DFS) algorithm to a file "Question6.txt".
with open("Question6.txt", "w") as f:
    for h in range(height):
        for w in range(width):
            f.write("1" if (h, w) in visited else "0")
            # Write "1" to the file if the square (h, w) is visited; otherwise, write "0".
            # If it's not the last element in the row (column), write a comma (",") to separate the values.
            if w != width - 1:
                f.write(",")
                # Move to the next line after each row is written.
        f.write("\n")


# The following lines of code are used for Part2 of P5
# Calculate the Manhattan distances (distance from each square to the goal) and store them in the 'man' dictionary.
# The 'math.sqrt' function is used to compute the square root.
man = {(i,j): abs(i-(height - 1)) + abs(j-center_idx) for j in range(width) for i in range(height)}
euc = {(i,j): math.sqrt((i-(height-1))*2 + (j-center_idx)*2 ) for j in range(width) for i in range(height)}

# Save the Manhattan distances to the goal for each square in a CSV format to the file "Question7.txt".
with open("Question7.txt", "w") as f:
    for h in range(height):
        for w in range(width):
            # Write the Manhattan distance value for the current square (h, w) to the file.
            f.write(str(man[(h, w)]))
            # If it's not the last element in the row (column), write a comma (",") to separate the values.
            if w != width - 1:
                f.write(",")
                # Move to the next line after each row is written.
        f.write("\n")


# First, we define the A* search algorithm function with parameters: height, width, dist_method, man, euc.
def a_star_search(height, width, dist_method, man, euc):
    # Create a dictionary 'g' to store the cost of reaching each cell from the starting cell.

    g = {(i,j): float('inf') for j in range(width) for i in range(height)}
    g[(0, center_idx)] = 0

    queue = [(0,center_idx)]
    visited = set()

    # Perform the A* search while there are cells in the queue to explore,
    # and the goal cell (height - 1, center_idx) has not been visited yet.
    while queue and (height - 1,center_idx) not in visited:
        if dist_method == 'manhattan':
            queue.sort(key=lambda x: g[x] + man[x])
        elif dist_method == 'euclidean':
            queue.sort(key=lambda x: g[x] + euc[x])
        else:
            print('distance method should be either mahattan or euclidean!')
        point = queue.pop(0)
        if point not in visited:
            visited.add(point)
            i, j = point[0], point[1]
            succ = cells[i][j].succ
            if 'U' in succ and (i-1,j) not in visited:
                if (i-1,j) not in queue: queue += [(i-1,j)]
                g[(i-1,j)] = min(g[(i-1,j)], g[(i,j)]+1)
            if 'D' in succ and (i+1,j) not in visited:
                if (i+1,j) not in queue: queue += [(i+1,j)]
                g[(i+1,j)] = min(g[(i+1,j)], g[(i,j)]+1)
            if 'L' in succ and (i,j-1) not in visited:
                if (i,j-1) not in queue: queue += [(i,j-1)]
                g[(i,j-1)] = min(g[(i,j-1)], g[(i,j)]+1)
            if 'R' in succ and (i,j+1) not in visited:
                if (i,j+1) not in queue: queue += [(i,j+1)]
                g[(i,j+1)] = min(g[(i,j+1)], g[(i,j)]+1)
    return visited

# list of squares searched by A* with Manhattan distance to the goal as the heuristic
a_star_man_visited = a_star_search(height, width, 'manhattan', man, euc)

# list of squares searched by A* with Euclidean distance to the goal as the heuristic
a_star_euclidean_visited = a_star_search(height, width, 'euclidean', man, euc)

# The following lines of code are used to generate the output for question 8 & question 9
# Open the file "Question8.txt" in write mode ('w').
# The 'with' statement ensures that the file is automatically closed after the block of code is executed.
# The file will be created if it doesn't exist or overwritten if it already exists.
with open("Question8.txt", "w") as f:
    # Iterate over the 'height' range.
    for h in range(height):
        for w in range(width):
            f.write("1" if (h, w) in a_star_man_visited else "0")
            if w != width - 1:
                f.write(",")
        f.write("\n")

# Open the file "Question9.txt" in write mode ('w').
# The 'with' statement ensures that the file is automatically closed after the block of code is executed.
# The file will be created if it doesn't exist or overwritten if it already exists.
with open("Question9.txt", "w") as f:
    # Iterate over the 'height' range.
    for h in range(height):
        for w in range(width):
            f.write("1" if (h, w) in a_star_euclidean_visited else "0")
            if w != width - 1:
                f.write(",")
        f.write("\n")
