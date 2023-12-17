from collections import deque


class Node:
    complete_path = ""

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
            print(self.row, self.col, direction)
            Node.complete_path = direction + Node.complete_path
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
    last_node = 0
    queue = deque([(start_node, 500)])
    while queue:
        current_node, total_energy = queue.popleft()
        successor(current_node, grid)
        for neighbor in current_node.children:
            if (not neighbor.isVisited) & (neighbor.isOpen):
                neighbor.isVisited = True
                total_energy += neighbor.boost - neighbor.energy_cost
                queue.append((neighbor, total_energy))
                last_node = neighbor
                if neighbor.isTarget:
                    targets -= 1
                    last_node.path()
                    print(Node.complete_path)

        if targets == 0:
            break


margins = input("How many rows and columns does the map have? (e.g. 5 8): ").split()
row = int(margins[0])
col = int(margins[1])


def mysplit(s):
    cost = s.rstrip("CBITR")
    boost = s[len(cost) :]
    return cost, boost


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
# print(targets)
bfs(start_node, grid, targets)
# for i in range(row):
#     for j in range(col):
#         print(grid[i][j], end="\n")
#     print()

print(Node.complete_path)
