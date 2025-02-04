"""
Advent of Code day 20 part 1
Written by Trevor Ferris
2/3/2025
"""

from enum import StrEnum
from time import time

MAZE_FILENAME = "Aoc20/input.txt"
BAD_MAZE = 100000
MIN_SAVE = 100
DIRS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
J_DIRS = [(2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]

class M_type(StrEnum):
    WALL = "#"
    EMPTY = "."
    START = "S"
    END = "E"

class M_tile(object):
    def __init__(self, x: int, y: int, type: M_type):
        self.x = x
        self.y = y
        self.type = type
        if type == M_type.START:
            self.cost = 0
        else:
            self.cost = BAD_MAZE
    
    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def get_type(self) -> M_type:
        return self.type
    
    def get_cost(self) -> int:
        return self.cost
    
    def set_cost(self, cost: int):
        self.cost = cost

    def set_type(self, type: M_type):
        self.type = type

    def copy(self):
        return M_tile(self.x, self.y, self.type)

def load_maze(file_name: str) -> tuple[list[list[M_tile]], tuple[int, int]]:
    """Loads maze and start position from file"""
    maze = []
    with open(file_name, "r") as maze_file:
        for x, row in enumerate(maze_file):
            m_row = []
            row = row.rstrip("\n")
            for y, col in enumerate(row):
                if col == M_type.START:
                    start_pos = (x, y)
                m_row.append(M_tile(x, y, col))
            maze.append(m_row)
    return maze, start_pos

def print_maze(maze: list[list[M_tile]]):
    """Print maze for debugging"""
    for row in maze:
        print("".join(str(ch.get_type()) for ch in row))

def copy_maze(maze: list[list[M_tile]]) -> list[list[M_tile]]:
    """Deepcopy maze"""
    new_maze = []
    for row in maze:
        new_row = [tile.copy() for tile in row]
        new_maze.append(new_row)
    return new_maze

def find_tile_costs(maze: list[list[M_tile]], start_pos: tuple[int, int]) -> list[list[M_tile]]:
    """Run the maze and set the time to reach each tile as you go"""
    pos = start_pos
    cost = 0
    while maze[pos[0]][pos[1]].get_type() != M_type.END:
        cost += 1
        for dir in DIRS:
            if (maze[pos[0] + dir[0]][pos[1] + dir[1]].get_type() != M_type.WALL and
                maze[pos[0] + dir[0]][pos[1] + dir[1]].get_cost() > maze[pos[0]][pos[1]].get_cost()):
                pos = (pos[0] + dir[0], pos[1] + dir[1])
        maze[pos[0]][pos[1]].set_cost(cost)
    return maze

def find_shortcuts(maze: list[list[M_tile]], start_pos: tuple[int, int]):
    """Run maze and at each position check the 8 jumpable directions and if a value saves enough time record it"""
    pos = start_pos
    while maze[pos[0]][pos[1]].get_type() != M_type.END:
        for j_dir in J_DIRS:
            if 0 <= pos[0] + j_dir[0] < len(maze) and  0 <= pos[1] + j_dir[1] < len(maze[0]):
                if (maze[pos[0] + j_dir[0]][pos[1] + j_dir[1]].get_type() != M_type.WALL and
                    maze[pos[0] + j_dir[0]][pos[1] + j_dir[1]].get_cost() >= maze[pos[0]][pos[1]].get_cost() + MIN_SAVE + 2):
                    yield 1
        for dir in DIRS:
            if (maze[pos[0] + dir[0]][pos[1] + dir[1]].get_type() != M_type.WALL and
                maze[pos[0] + dir[0]][pos[1] + dir[1]].get_cost() > maze[pos[0]][pos[1]].get_cost()):
                new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        pos = new_pos
    return 0 

def main():
    start_time = time()
    maze, start_pos = load_maze(MAZE_FILENAME)
    maze = find_tile_costs(copy_maze(maze), start_pos)
    print(f"Number of {MIN_SAVE}ps or more shortcuts {sum(find_shortcuts(maze, start_pos))}")
    end_time = time()
    print(f"Time:{end_time - start_time}")

if __name__ == ("__main__"):
    main()