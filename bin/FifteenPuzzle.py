import random
import copy
import time

# Mengembalikan puzzle berupa list 2 dimensi dari file di path
def read_puzzle_from_file(path):
    with open(path) as f:
        return [[int(x) for x in line.split()] for line in f]

# Mengembalikan puzzle berupa list 2 dimensi secara random
def generate_random_puzzle():
    nums = [i for i in range(1, 17)]
    return [[nums.pop(random.randint(0, len(nums) - 1)) for _ in range(4)] for _ in range(4)]

# Print matrix puzzle
def print_puzzle(puzzle):
    for row in puzzle:
        for tile in row:
            if (tile == 16):
                print("_   ", end="")
            else:
                print(str(tile) + ("   " if tile < 10 else "  "), end="")
        print()

# Print solusi dari tree dan node solusi puzzle
def print_path(tree, solved):
    path = []
    while (solved[2] != -1):
        path.append(solved)
        solved = tree[solved[2]]
    path.append(tree[0])
    path.reverse()
    for state in path:
        print("Langkah ke-" + str(state[3]) + ": " + state[5])
        print_puzzle(state[0])
        print()

# Mengembalikan nilai fungsi KURANG(i) dari puzzle
def kurang(i, puzzle):
    count = 0
    found = False
    for row in range(0, 4):
        for col in range(0, 4):
            if (not found):
                found = puzzle[row][col] == i
            else:
                if (puzzle[row][col] < i):
                    count += 1
    return count

# Mengembalikan letak kotak kosong pada puzzle
def get_blank_tile(puzzle):
    blank_row = 0
    blank_col = 0
    for row in range(0, 4):
        for col in range(0, 4):
            if (puzzle[row][col] == 16):
                blank_row = row
                blank_col = col
    return blank_row, blank_col

# Mengembalikan apakah puzzle bisa di-solve atau tidak, juga nilai jumlah KURANG + X
def is_solvable(puzzle):
    total = 0
    for i in range(1, 17):
        total += kurang(i, puzzle)

    blank_row, blank_col = get_blank_tile(puzzle)
    x = 0 if ((blank_row + blank_col) % 2 == 0) else 1

    print("Nilai jumlah kurang + x: ", total + x, end="")
    return (total + x) % 2 == 0, total + x

# Mengembalikan apakah puzzle sudah di-solve atau belum
def is_solved(puzzle):
    return puzzle == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

# Mengembalikan estimasi cost dari state puzzle sekarang ke solusi
def estimate_cost(puzzle):
    cost = 0
    supposed = 1
    for row in range(0, 4):
        for col in range(0, 4):
            if (puzzle[row][col] != supposed):
                cost += 1
            supposed += 1
    return cost

# Mengembalikan index node dengan nilai cost terkecil
def get_cheapest_node_index(queue):
    costs = [q[1] for q in queue]
    return costs.index(min(costs))

# Mengembalikan list dari semua node yang dapat di-capai dari dari state puzzle sekarang
def get_possible_nodes(node, tree, parent_idx, index_count):
    nodes = []
    blank_row, blank_col = get_blank_tile(node[0])
    depth = node[3] + 1
    if (blank_row > 0):
        up = copy.deepcopy(node[0])
        up[blank_row][blank_col] = up[blank_row - 1][blank_col]
        up[blank_row - 1][blank_col] = 16
        nodes.append([up, depth + estimate_cost(up), parent_idx, depth, index_count[0], "UP"])
        index_count[0] += 1
    if (blank_row < 3):
        down = copy.deepcopy(node[0])
        down[blank_row][blank_col] = down[blank_row + 1][blank_col]
        down[blank_row + 1][blank_col] = 16
        nodes.append([down, depth + estimate_cost(down), parent_idx, depth, index_count[0], "DOWN"])
        index_count[0] += 1
    if (blank_col > 0):
        left = copy.deepcopy(node[0])
        left[blank_row][blank_col] = left[blank_row][blank_col - 1]
        left[blank_row][blank_col - 1] = 16
        nodes.append([left, depth + estimate_cost(left), parent_idx, depth, index_count[0], "LEFT"])
        index_count[0] += 1
    if (blank_col < 3):
        right = copy.deepcopy(node[0])
        right[blank_row][blank_col] = right[blank_row][blank_col + 1]
        right[blank_row][blank_col + 1] = 16
        nodes.append([right, depth + estimate_cost(right), parent_idx, depth, index_count[0], "RIGHT"])
        index_count[0] += 1
    return nodes

# Solve 15-Puzzle dengan Branch and Bound
def solve(puzzle):
    tree = []
    queue = []
    root = [puzzle, 0, -1, 0, 0, "START"] # Node = [Puzzle, Cost, Parent Node Index, Depth, Index, Step]
    tree.append(root)
    queue.append(root)
    index_count = [1]
    visited = 1
    while (len(queue) > 0):
        now = queue.pop(get_cheapest_node_index(queue))
        print("\r",end='')
        print("Nodes visited: " + str(visited) 
            + " Now cost: " + str(now[1] - now[3]) 
            + " Depth: " + str(now[3]), end="  ")
        visited += 1
        if (is_solved(now[0])):
            return tree, now
        else:
            parent_idx = now[4]
            possible_nodes = get_possible_nodes(now, tree, parent_idx, index_count)
            for node in possible_nodes:
                tree.append(node)
                queue.append(node)
    return NULL, NULL

# Program utama
def main():
    print("Apakah ingin membuka puzzle dari file? (y/n): ", end="")
    choice = input()

    if (choice == "y"):
        print("Masukkan nama file: ", end="")
        filename = input()
        puzzle = read_puzzle_from_file("puzzles/" + filename)
    else:
        print("Masukkan kesulitan maks. puzzle random: ", end="")
        difficulty = int(input())
        puzzle = generate_random_puzzle()
        while (is_solvable(puzzle)[1] > difficulty):
            print("\r",end='')
            puzzle = generate_random_puzzle()

    print("\nPosisi awal puzzle:")
    print_puzzle(puzzle)
    print()

    for i in range(1, 17):
        print("KURANG("+str(i)+"):", kurang(i, puzzle))

    if (not is_solvable(puzzle)[0]):
        print("\nPuzzle ini tidak dapat diselesaikan.")
    else:
        print()
        start = time.time()
        tree, solved = solve(puzzle)
        end = time.time()

        print("\n\nAlur solusi puzzle:\n")
        print_path(tree, solved)
        print("Waktu eksekusi:", round(end - start, 6), end="s\n")
        print("Jumlah simpul yang dibangkitkan:", len(tree))

if __name__ == "__main__":
    main()