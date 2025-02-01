"""
Advent of Code Day 16 Part 1
Written by Trevor Ferris
1/31/2025
"""
import sys
sys.setrecursionlimit(2000)

from enum import StrEnum, IntEnum

MAZE_FILENAME = "Aoc16/input.txt"
DIRS = []
INIT_FACING = ">"
BAD_MAZE = 10000000000
MOVE_COST = 1
TURN_COST = 1000

class M_obj(StrEnum):
    WALL = "#"
    EMPTY = "."
    START = "S"
    END = "E"

class Rotation(IntEnum):
    CW = 3
    BKW = 2
    CCW = 1

class Facing(StrEnum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"
       
def load_maze(file_name: str):
    """Builds maze from given file"""
    maze = []
    with open(file_name, "r") as maze_file:
        for x, row in enumerate(maze_file):
            maze_row = []
            row = row.rstrip("\n")
            for y, col in enumerate(row):
                if col == M_obj.START:
                    start_pos = (x, y)
                maze_row.append(col)
            maze.append(maze_row)
    return maze, start_pos

def maze_copy(maze):
    new_maze = []
    for row in maze:
        maze_row = [ch for ch in row]
        new_maze.append(maze_row)
    return new_maze

def print_maze(maze: list[list[M_obj]]):
    """Print maze for debugging"""
    for row in maze:
        print("".join(ch for ch in row))

def dir_check(dir: Facing) -> tuple[int, int]:
    """Gives coordinate movement of given direction"""
    match dir:
        case Facing.NORTH:
            return (-1, 0)
        case Facing.SOUTH:
            return (1, 0)
        case Facing.EAST:
            return (0, 1)
        case Facing.WEST:
            return (0, -1)

def rot_dir(dir: Facing, rot: Rotation):
    facings = list(Facing)
    return facings[facings.index(dir) - rot]

def check_next(maze: list[list[str]], pos, dir):
    new_pos = dir_check(dir)
    if maze[pos[0] + new_pos[0]][pos[1] + new_pos[1]] not in  (M_obj.EMPTY, M_obj.END):
        return False
    return True

def run_maze(maze: list[list[str]], pos: tuple[int, int], dir: Facing):   
    if maze[pos[0]][pos[1]] == M_obj.END:
        print_maze(maze)
        return 0
    maze[pos[0]][pos[1]] = dir
    if check_next(maze, pos, dir):
        fwd = dir_check(dir)
        y1 = MOVE_COST + run_maze(maze_copy(maze), (pos[0] + fwd[0], pos[1] + fwd[1]), dir)
    else:
        y1 = BAD_MAZE
    if check_next(maze, pos, clock := rot_dir(dir, Rotation.CW)):
        cw = dir_check(clock)
        y2 = TURN_COST + MOVE_COST + run_maze(maze_copy(maze), (pos[0] + cw[0], pos[1] + cw[1]), clock)
    else:
        y2 = BAD_MAZE
    if check_next(maze, pos, counter := rot_dir(dir, Rotation.CCW)):
        ccw = dir_check(counter)
        y3 = TURN_COST + MOVE_COST + run_maze(maze_copy(maze), (pos[0] + ccw[0], pos[1] + ccw[1]), counter)
    else:
        y3 = BAD_MAZE
    return min(y1, y2, y3)         
   
def main():
    maze, start_pos = load_maze(MAZE_FILENAME)
    print(list(Facing))
    print_maze(maze)
    print(run_maze(maze, start_pos, INIT_FACING))

if __name__ == ("__main__"):
    main()