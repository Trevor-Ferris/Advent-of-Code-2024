"""
Advent of Code Problem 15 part 1
Written by Trevor Ferris
1/29/2025
"""

from typing import Iterator

MAP_FILENAME = "input.txt"
DIRS = [">", "<", "v", "^"]

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
                    case "@":
                        w_row.append(w_obj(x, y, pos))
                        r_start = (x, y)
                    case "O":
                        w_row.append(w_obj(x, y, pos))
                    case "#":
                        w_row.append(w_obj(x, y, pos))
                    case ".":
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
        case "^":
            return (-1, 0)
        case "v":
            return (1, 0)
        case "<":
            return (0, -1)
        case ">":
            return (0, 1)
        
def print_map(w_map: list[list[w_obj]]):
    """Prints map for testing purposes"""
    for row in w_map:
        s = ""
        for col in row:
            s = s + col.type_of()
        print(s)

def check_next(pos: tuple[int, int], dir_x: int, dir_y: int, w_map: list[list[w_obj]]) -> bool:
    """
        Checks the next position until it either hits a wall or an empty space

        Args:
            pos: The current position (x, y)
            dir_x: The direction the object is being pushed up or down
            dir_y: The direction the object is being pushed left or right
            w_map: 2D list of objects representing a map of the warehouse 

        Returns a bool of whether the robot should push the block, as well as moving the objects appropriately
    
    """
    match w_map[pos[0] + dir_x][pos[1] + dir_y].type_of():
        case "#":
            return False
        case "O":
            if check_next((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map):
                swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
                return True
            else:
                return False
        case ".":          
            swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
            return True

def swap_obj(pos1, pos2, w_map):
    """Switches position of two objects in the map"""
    w_map[pos1[0]][pos1[1]], w_map[pos2[0]][pos2[1]] = w_map[pos2[0]][pos2[1]], w_map[pos1[0]][pos1[1]]

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
    match w_map[pos[0] + dir_x][pos[1] + dir_y].type_of(): 
        case "#":
            return pos
        case "O":
            if check_next((pos[0] + dir_x, pos[1] + dir_y), dir_x, dir_y, w_map):
                swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
                return (pos[0] + dir_x, pos[1] + dir_y)
            else:
                return pos
        case ".":
            swap_obj(pos, (pos[0] + dir_x, pos[1] + dir_y), w_map)
            return (pos[0] + dir_x, pos[1] + dir_y)

def read_directions(w_map: list[list[w_obj]], moves: list[str], r_pos: tuple[int, int]):
    """Reads the list of moves and moves the robot in the direction returns the new map"""
    for move in moves:
        r_pos = move_robot(r_pos, w_map, move)
    return w_map

def sum_coords(fin_map: list[list[w_obj]]) -> Iterator:
    for x, row in enumerate(fin_map):
        for y, col in enumerate(row):
            if col.type_of() == "O":
                yield 100 * x + y

def main():
    w_map, moves, r_start = load_map(MAP_FILENAME)
    fin_map = read_directions(warehouse_copy(w_map), moves, r_start)
    print(sum(sum_coords(fin_map)))

if __name__ == ("__main__"):
    main()
            
