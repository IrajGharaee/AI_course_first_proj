from collections import deque


class Node:
    complete_path = []
    energy = 500

    @staticmethod
    def boosters(boost):
        if boost == "C":
            return 10, False
        elif boost == "B":
            return 5, False
        elif boost == "I":
            return 12, False
        elif boost == "T":
            return 0, True
        else:
            return 0, False

    def __init__(self, row, col, energy_cost, boost=None):
        if energy_cost == "X":
            self.energy_cost = 0
            self.isOpen = False
            self.boost, self.isTarget = Node.boosters(boost)
        else:
            self.energy_cost = int(energy_cost)
            self.isOpen = True
            self.boost, self.isTarget = Node.boosters(boost)
        self.row = row
        self.col = col
        self.isVisited = False
        self.children = []
        self.parent = []

    def path(self, p=""):
        if not isinstance(self.parent, list) and self.parent:
            parent_node, direction = self.parent
            print(direction + "\n", self.row, self.col)
            Node.energy = Node.energy + self.boost - self.energy_cost
            Node.complete_path.append([direction, self.boost - self.energy_cost])
            parent_node.path()

    def add_children(self, child, direction):
        self.children.append(child)
        child.add_parent(self, direction)

    def add_parent(self, parent, direction):
        self.parent = (parent, direction)

    def __str__(self):
        return f"[({self.row},{self.col})| {self.energy_cost}| {self.boost}| {self.isOpen}| {self.isTarget}]"


directions = [((-1, 0), "U"), ((1, 0), "D"), ((0, -1), "L"), ((0, 1), "R")]


def successor(node, grid):
    rows = len(grid)
    cols = len(grid[0])
    for direction in directions:
        new_row = node.row + direction[0][0]
        new_col = node.col + direction[0][1]
        if (0 <= new_row < rows) & (0 <= new_col < cols):
            if not grid[new_row][new_col].isVisited:
                node.add_children(grid[new_row][new_col], direction[1][0])
    return


def bfs(start_node, grid, targets):
    queue = deque([start_node])
    while queue:
        current_node = queue.popleft()
        successor(current_node, grid)
        for neighbor in current_node.children:
            if (not neighbor.isVisited) & (neighbor.isOpen):
                neighbor.isVisited = True
                queue.append(neighbor)
                if neighbor.isTarget:
                    targets -= 1
                    Node.complete_path.append(
                        f"Target ({current_node.row}, {current_node.col} reached)"
                    )
                    neighbor.isTarget = False

        if targets == 0:
            break


def dfs(start_node, targets, grid):
    stack = [start_node]
    start_node.isVisited = True
    x = 0
    while stack:
        current_node = stack.pop()
        x = x + 1
        if current_node.isTarget:
            Node.complete_path.append(
                f"Target ({current_node.row}, {current_node.col} reached)"
            )
            targets -= 1
            current_node.isTarget = False

        if targets == 0:
            current_node.path()
            return True

        successor(current_node, grid)
        for child in current_node.children[::-1]:
            if not child.isVisited and child.isOpen:
                stack.append(child)
                child.isVisited = True
    if len(all_paths) == 0:
        print("No solution found")
        return False


margins = input("How many rows and columns does the map have? (e.g. 5 8): ").split()
row = int(margins[0])
col = int(margins[1])


def mysplit(s):
    cost = s.rstrip("CBITR")
    boost = s[len(cost) :]
    return cost, boost


all_paths = []
targets = 0
grid = []
for i in range(row):
    tmp = input().split()
    for j in range(col):
        cost, boost = mysplit(tmp[j])
        if "T" in tmp[j]:
            targets += 1
        tmp[j] = Node(i, j, cost, boost)
    grid.append(tmp)

start_node = grid[0][0]
start_node.isVisited = True
# bfs(start_node, grid, targets)

# targets = 0
# grid = []
# for i in range(row):
#     tmp = input().split()
#     for j in range(col):
#         cost, boost = mysplit(tmp[j])
#         if "T" in tmp[j]:
#             targets += 1
#         tmp[j] = Node(i, j, cost, boost)
#     grid.append(tmp)

dfs(start_node, targets, grid)
print((Node.complete_path)[::-1])
