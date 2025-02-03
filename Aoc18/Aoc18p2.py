"""
Advent of Code day 18 part 1
Written by Trevor Ferris
2/2/2025
Notes: Spent a lot of time trying to figure out a way to do it with only running the maze one time and gave up eventually
surprised at how fast the bisection search ended up though
"""

import sys
from enum import StrEnum
from time import time

sys.setrecursionlimit(2000)

COORD_FILENAME = "Aoc18/input.txt"
MAP_SIZE = 70
NUM_BYTES = 3450
NOT_VISITED = 10000
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class M_type(StrEnum):
    WALL = "#"
    EMPTY = "."

class Maze_tile(object):
    def __init__(self, type):
        self.type = type
        self.travel_cost = NOT_VISITED
    
    def get_type(self):
        return self.type

    def is_empty(self):
        return self.type == M_type.EMPTY

    def get_travel_cost(self):
        return self.travel_cost
    
    def set_type(self, type: str):
        self.type = type

    def set_travel_cost(self, cost: int):
        self.travel_cost = cost

def load_bytes(file_name: str) -> list[tuple[int, int]]:
    """Loads the list of Bytes from file"""
    bytes = []
    with(open(file_name, "r")) as byte_file:
        for line in byte_file:
            pos = tuple(map(int, line.split(",")))
            bytes.append(pos)
    return bytes

def print_maze(maze: list[list[Maze_tile]]):
    """Print maze for debugging"""
    for x in maze:
        print("".join(ch.get_type() for ch in x))

def build_maze(bytes: list[tuple[int, int]]) -> list[list[Maze_tile]]:
    """Builds a maze of MAP_SIZE x MAP_SIZE with the bytes as walls"""
    maze = []
    bytes = bytes[:NUM_BYTES]
    for y in range(MAP_SIZE + 1):
        maze_row = []
        for x in range(MAP_SIZE + 1):
            if (x, y) in bytes:
                maze_row.append(Maze_tile(M_type.WALL))
            else:
                maze_row.append(Maze_tile(M_type.EMPTY))
        maze.append(maze_row)
    return maze

def check_next(next: Maze_tile, cost: int) -> bool:
    """Checks if the next maze tile is not a wall and is cheaper to get to with the current path"""
    if next.is_empty() and cost < next.get_travel_cost():
        return True
    return False

def find_maze(maze: list[list[Maze_tile]], x: int, y: int, cost: int):
    """Sets the travel cost of each reachable tile to the number of moves needed to reach it"""
    maze[x][y].set_travel_cost(cost)
    if x == MAP_SIZE and y == MAP_SIZE:
        return True
    for dir in DIRS:
        if 0 <= x + dir[0] <= MAP_SIZE and 0 <= y + dir[1] <= MAP_SIZE:
            if check_next(maze[x + dir[0]][y + dir[1]], cost + 1):
                find_maze(maze, x + dir[0], y + dir[1], cost + 1)

def maze_search(bytes):
    """Bisection search for the last completable maze"""
    b_high = NUM_BYTES
    b_low = 0
    while True:
        if (b_high + b_low) // 2 == b_low:
            return bytes[b_low]
        print(f"Testing {(b_high + b_low) // 2}...")
        maze = build_maze(bytes[:((b_high + b_low) // 2)])
        find_maze(maze, 0, 0, 0)
        if maze[MAP_SIZE][MAP_SIZE].get_travel_cost() == NOT_VISITED:
            b_high = (b_high + b_low) // 2
        else:
            b_low = (b_high + b_low) // 2

def main():
    start_time = time()
    bytes = load_bytes(COORD_FILENAME)
    print(f"First byte that makes an unsolvable maze: {maze_search(bytes)}")
    end_time = time()
    print(f"Run time: {end_time - start_time}")

if __name__ == ("__main__"):
    main()