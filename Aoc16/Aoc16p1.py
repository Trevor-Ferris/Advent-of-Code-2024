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
    CCW = 1

class Facing(StrEnum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"

class Maze_tile(object):
    def __init__(self, type):
        self.type = type
        self.score = BAD_MAZE

    def get_type(self):
        return self.type

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
    
    def set_type(self, type):
        self.type = type
      
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
                if col == M_obj.END:
                    end_pos = (x, y)
                maze_row.append(Maze_tile(col))
            maze.append(maze_row)
    return maze, start_pos, end_pos

def maze_copy(maze):
    new_maze = []
    for row in maze:
        maze_row = [ch for ch in row]
        new_maze.append(maze_row)
    return new_maze

def print_maze(maze: list[list[Maze_tile]]):
    """Print maze for debugging"""
    for row in maze:
        print("".join(ch.get_type() for ch in row))

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

def check_wall(maze: list[list[Maze_tile]], pos, dir):
    new_pos = dir_check(dir)
    if maze[pos[0] + new_pos[0]][pos[1] + new_pos[1]].get_type() != M_obj.WALL:
        return True
    return False

def run_maze(maze: list[list[Maze_tile]], pos: tuple[int, int], dir: Facing, tile_score: int, turned: bool):   
    while True:
        #check potential turns and call run maze with the turned direction
        if not turned:    
            if check_wall(maze, pos, cw := rot_dir(dir, Rotation.CW)):
                run_maze(maze, pos, cw, tile_score + TURN_COST, True)
            if check_wall(maze, pos, ccw := rot_dir(dir, Rotation.CCW)):
                run_maze(maze, pos, ccw, tile_score + TURN_COST, True)
        #check if the next object is a wall break if so
        turned = False
        if not check_wall(maze, pos, dir):
            break
        #Check if the next tile has a higher score than the current tile_score 
        fwd = dir_check(dir)
        if tile_score + MOVE_COST < maze[pos[0] + fwd[0]][pos[1] + fwd[1]].get_score():
        #Update the value to the current value if it is lower
            maze[pos[0] + fwd[0]][pos[1] + fwd[1]].set_score(tile_score + MOVE_COST)
            pos = (pos[0] + fwd[0], pos[1] + fwd[1])
            tile_score += MOVE_COST         
        #Break if higher
        else:
            break
 
def main():
    maze, start_pos, end_pos = load_maze(MAZE_FILENAME)
    print(list(Facing))
    print_maze(maze)
    run_maze(maze, start_pos, INIT_FACING, 0, False)
    print(maze[end_pos[0]][end_pos[1]].get_score())
if __name__ == ("__main__"):
    main()