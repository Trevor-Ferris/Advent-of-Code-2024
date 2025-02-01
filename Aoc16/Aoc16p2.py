"""
Advent of Code Day 16 Part 2
Written by Trevor Ferris
1/31/2025
"""

from enum import StrEnum, IntEnum

MAZE_FILENAME = "Aoc16/input.txt"
DIRS = []
INIT_FACING = ">"
BAD_MAZE = 100000
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

class Maze_tile(object):
    """
    Object of each map tile

    Args:
        type: Character from the maze
        score: Lowest cost to reach this tile
        opt: If the tile is in the optimal path to the end
    """
    def __init__(self, type: str):
        self.type = type
        self.score = BAD_MAZE
        self.opt = False

    def get_type(self):
        return self.type

    def get_score(self):
        return self.score

    def get_opt(self):
        return self.opt
    
    def set_score(self, score: int):
        self.score = score
    
    def set_type(self, type: str):
        self.type = type

    def set_opt(self):
        self.opt = True

def load_maze(file_name: str):
    """Builds maze from given file"""
    maze = []
    with open(file_name, "r") as maze_file:
        for x, row in enumerate(maze_file):
            maze_row = []
            row = row.rstrip("\n")
            for y, col in enumerate(row):
                maze_row.append(Maze_tile(col))
                if col == M_obj.START:
                    start_pos = (x, y)
                    maze_row[y].set_score(0)
                if col == M_obj.END:
                    end_pos = (x, y)
            maze.append(maze_row)
    return maze, start_pos, end_pos

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

def rot_dir(dir: Facing, rot: Rotation) -> Facing:
    """Rotates a direction by the given value"""
    facings = list(Facing)
    return facings[facings.index(dir) - rot]

def check_wall(maze: list[list[Maze_tile]], pos, dir):
    """Checks if the next position in the maze is a wall"""
    new_pos = dir_check(dir)
    if maze[pos[0] + new_pos[0]][pos[1] + new_pos[1]].get_type() != M_obj.WALL:
        return True
    return False

def run_maze(maze: list[list[Maze_tile]], pos: tuple[int, int], dir: Facing, tile_score: int, turned: bool):   
    """
    Runs through the tiles in the maze finding the lowest movement cost to reach each tile
    
    Args:
        maze: maze from input file
        pos: the current position
        dir: the current direction
        tile_score: the cost to reach this tile
        turned: whether or not the current recursion has turned on this tile

    Returns: Nothing, but modifies the Maze_tiles in maze
    """
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

def find_low_dir(maze, pos, cur_dir):
    """Finds the directions which the next values are lowest at an intersection"""
    dir_vals = []
    for dir in list(Facing):   
        if rot_dir(cur_dir, Rotation.BKW) != dir:
            dir_pos = dir_check(dir)
            dir_vals.append((maze[pos[0] + dir_pos[0]][pos[1] + dir_pos[1]].get_score(), dir))
    low_val =  min(val[0] for val in dir_vals)
    for dir in dir_vals:
        if dir[1] == cur_dir:
            if dir[0] == (low_val + TURN_COST):
                yield dir[1]
        if dir[0] == low_val:
            yield dir[1]

def find_best(maze, pos, dir):
    """Runs the maze in reverse direction finding the paths which contain the lowest scores"""
    #Find all directions that have the lowest adjacent score
    maze[pos[0]][pos[1]].set_opt()
    yield 1
    if maze[pos[0]][pos[1]].get_type() == M_obj.START:
        maze[pos[0]][pos[1]].set_type("O")
        return
    maze[pos[0]][pos[1]].set_type("O")
    for dir in find_low_dir(maze, pos, dir):
        #check if the path has already been checked
        dir_pos = dir_check(dir)
        if maze[pos[0] + dir_pos[0]][pos[1] + dir_pos[1]].get_opt():
            continue
        yield from find_best(maze, (pos[0] + dir_pos[0], pos[1] + dir_pos[1]), dir)

def main():
    maze, start_pos, end_pos = load_maze(MAZE_FILENAME)
    print("Running maze...")
    run_maze(maze, start_pos, INIT_FACING, 0, False)
    print("Lowest score:", maze[end_pos[0]][end_pos[1]].get_score())
    print("Number of optimal tiles:", sum(find_best(maze, end_pos, INIT_FACING)))

if __name__ == ("__main__"):
    main()