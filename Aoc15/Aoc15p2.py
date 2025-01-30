"""
Advent of Code Problem 15 part 2
Written by Trevor Ferris
1/29/2025
"""

from typing import Iterator
from enum import StrEnum

MAP_FILENAME = "input.txt"
DIRS = [">", "<", "v", "^"]

class Ob_type(StrEnum):
    ROBOT = "@"
    WALL = "#"
    BOX = "O"
    L_BOX = "["
    R_BOX  = "]"
    EMPTY  = "."

class Moving(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

class w_obj(object):
    """Class containing the position of the object and what type of object it is"""
    def __init__(self, x, y, ch):
        self.x = x
        self.y = y
        self.type = ch
    
    def type_of(self) -> str:
       return self.type

def load_map(file_name: str) -> list[list[w_obj], list[str], tuple[int, int]]:
    """
        Loads the map and list of moves

        Returns: A 2D list of objects, a list of directions and the starting position of the robot
    """
    w_map = []
    moves = []
    with open(file_name, "r") as map_file:
        for x, line in enumerate(map_file):
            line = line.rstrip("\n")
            if not line:
                continue
            if line[0] in DIRS:
                moves.extend(ch for ch in line)
                continue
            w_row = []
            for y, pos in enumerate(line):
                match pos:
                    case Ob_type.ROBOT:
                        w_row.append(w_obj(x, y, pos))
                        w_row.append(w_obj(x, y, "."))
                        r_start = (x, 2 * y)
                    case Ob_type.BOX:
                        w_row.append(w_obj(x, y, "["))
                        w_row.append(w_obj(x, y, "]"))
                    case _:
                        w_row.append(w_obj(x, y, pos))
                        w_row.append(w_obj(x, y, pos))

            w_map.append(w_row)
    return w_map, moves, r_start

def warehouse_copy(w_map: list[list[w_obj]]) -> list[list[w_obj]]:
    """Returns a deepcopy of the warehouse"""
    new_w_map = []
    for row in w_map:
        w_row = [ch for ch in row]
        new_w_map.append(w_row)
    return new_w_map

def dir_check(dir: str) -> tuple[int, int]:
    """Gives coordinate movement of given direction"""
    match dir:
        case Moving.UP:
            return (-1, 0)
        case Moving.DOWN:
            return (1, 0)
        case Moving.LEFT:
            return (0, -1)
        case Moving.RIGHT:
            return (0, 1)

def find_half(half: Ob_type):
    """Returns the direction of the other half of the box"""
    if half == Ob_type.L_BOX:
        return dir_check(Moving.RIGHT)
    else:
        return dir_check(Moving.LEFT)
    
def swap_obj(pos1, pos2, w_map):
    """Switches position of two objects in the map"""
    w_map[pos1[0]][pos1[1]], w_map[pos2[0]][pos2[1]] = w_map[pos2[0]][pos2[1]], w_map[pos1[0]][pos1[1]]
            
def print_map(w_map: list[list[w_obj]]):
    """Prints map for testing purposes"""
    for row in w_map:
        s = ""
        for col in row:
            s = s + col.type_of()
        print(s)

def check_hor(pos: tuple[int, int], dir_x: int, dir_y: int, w_map: list[list[w_obj]]) -> bool:
    """
        Checks the next horizontal position until it either hits a wall or an empty space

        Args:
            pos: The current position (x, y)
            dir_x: The direction the object is being pushed up or down
            dir_y: The direction the object is being pushed left or right
            w_map: 2D list of objects representing a map of the warehouse 

        Returns: Whether or not the robot should push the block, as well as moving the objects if it should
    
    """
    match w_map[pos[0]][pos[1]].type_of():
        case Ob_type.ROBOT:
            if check_hor((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map):
                swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
                return True
            else:
                return False
        case Ob_type.L_BOX | Ob_type.R_BOX:
            if w_map[pos[0] + dir_x][pos[1] + dir_y].type_of() :
                if check_hor((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map):
                    swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
                    return True
                else:
                    return False
        case Ob_type.EMPTY:
            return True
        case Ob_type.WALL:
            return False
        
def check_vert(pos: tuple[int, int], dir_x: int, dir_y: int, w_map: list[list[w_obj]], box_check: bool) -> bool:
    """
        Checks the next horizontal position until it either hits a wall or an empty space

        Args:
            pos: The current position (x, y)
            dir_x: The direction the object is being pushed up or down
            dir_y: The direction the object is being pushed left or right
            w_map: 2D list of objects representing a map of the warehouse 
            box_check: Whether or not the current pos is a half of an already checked block
        
        Returns: Whether or not the robot should push the block
    
    """
    match w_map[pos[0]][pos[1]].type_of():
        case Ob_type.ROBOT:
            if check_vert((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map, False):
                return True
            else:
                return False
        case Ob_type.L_BOX | Ob_type.R_BOX:           
            if not box_check:
                box_dir = find_half(w_map[pos[0]][pos[1]].type_of())
                if (check_vert((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map, False) and
                    check_vert((pos[0] + box_dir[0], pos[1] + box_dir[1]), dir_x, dir_y, w_map, True)):
                    return True
            elif check_vert((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map, False):
                return True                
            return False
        case Ob_type.EMPTY:
            return True
        case Ob_type.WALL:
            return False

def move_vert(pos: tuple[int, int], dir_x: int, dir_y: int, w_map: list[list[w_obj]], box_check):
    """
        Moves the boxes ahead of the robot from furthest to closest

        Args:
            pos: The current position (x, y)
            dir_x: The direction the object is being pushed up or down
            dir_y: The direction the object is being pushed left or right
            w_map: 2D list of objects representing a map of the warehouse 
            box_check: Whether or not the current pos is a half of an already checked block
    
    """
    match w_map[pos[0]][pos[1]].type_of():
        case Ob_type.ROBOT:
            move_vert((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map, False)
            swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
        case Ob_type.L_BOX | Ob_type.R_BOX:           
            if not box_check:
                box_dir = find_half(w_map[pos[0]][pos[1]].type_of())
                move_vert((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map, False)
                move_vert((pos[0] + box_dir[0], pos[1] + box_dir[1]), dir_x, dir_y, w_map, True)
                swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
            else:
                move_vert((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map, False)
                swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)               
        case Ob_type.EMPTY:
            pass
        case Ob_type.WALL:
            pass

def move_robot(pos: tuple[int, int], w_map: list[list[w_obj]], dir: str):
    """
        Moves the robot in the given direction if the robot hits a wall or immovable object does nothing 
        otherwise moves the objects appropriately and gives the new position of the robot

        Args:
            pos: current position of the robot
            w_map: 2D list of objects representing the warehouse
            dir: arrow direction of the current instruction
        
        Returns: The coordinates of the robot after attempting the move
    """
    dir_x, dir_y = dir_check(dir)
    match dir:
        case Moving.LEFT | Moving.RIGHT:
            if check_hor(pos, dir_x, dir_y, w_map):
                return (pos[0] + dir_x, pos[1] + dir_y)
            else: 
                return pos
        case Moving.UP | Moving.DOWN:
            if check_vert(pos, dir_x, dir_y, w_map, False):
                move_vert(pos, dir_x, dir_y, w_map, False)
                return (pos[0] + dir_x, pos[1] + dir_y)
            else:
                return pos

def read_directions(w_map: list[list[w_obj]], moves: list[str], r_pos: tuple[int, int]):
    """Reads the list of moves and moves the robot in the direction returns the new map"""
    for move in moves:
        r_pos = move_robot(r_pos, w_map, move)
    print_map(w_map)
    return w_map

def sum_coords(fin_map: list[list[w_obj]]) -> Iterator:
    """Calculates the GPS score of a given map"""
    for x, row in enumerate(fin_map):
        for y, col in enumerate(row):
            if col.type_of() == Ob_type.L_BOX:
                yield 100 * x + y

def main():
    w_map, moves, r_start = load_map(MAP_FILENAME)
    fin_map = read_directions(warehouse_copy(w_map), moves, r_start)
    print("GPS Value:", sum(sum_coords(fin_map)))

if __name__ == ("__main__"):
    main()
            
