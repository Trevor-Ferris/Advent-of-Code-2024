"""
Advent of code day 10 problem 1
written by Trevor Ferris
1/23/2025
"""
from typing import Iterator

MAP_FILENAME = "input.txt"
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
HIGH_VAL = 9

def load_map(file_name: str) -> tuple[list[list[tuple]], list[tuple]]:
    """
    Builds a 2D list of the values in the map file name

    Args:
        file_name: the file name of the map file
    
    Returns:
        t_map: 2D list of tuples containing the value at each index 
        and a bool flag for if it has been visited
        trailheads: a list of coordinates where there is a trailhead
    """
    t_map = []
    trailheads = []
    with open(file_name, 'r') as map_file:
        for row, line in enumerate(map_file):
            line = line.rstrip('\n')
            c_vals = []
            for col, val in enumerate(line):
                c_vals.append((int(val), False))
                if val == "0":
                    trailheads.append((row,col))
            t_map.append(c_vals)
    return t_map, trailheads

def print_map(t_map: list):
    """Print the map for testing purposes"""
    for row in t_map:
        print(''.join(str(val) for (val, bool) in row))

def copy_map(t_map: list) -> list:
    """Returns a deep copy of the list"""
    return [row[:] for row in t_map]

def check_adj(pos: tuple, val: int, t_map: list) -> Iterator[int]:
    """
    Checks adjacent positions and advances if 1 level higher, yields 1 if at a 9

    Args:
        pos: tuple containing the map coordinates of the current position
        val: int of the value at the current map coordiates
        t_map: 2D list containing the topographical map
    
    Returns:
        A generator containing the score of the trailhead
    """
    t_map[pos[0]][pos[1]] = (val, True)
    if t_map[pos[0]][pos[1]][0] == HIGH_VAL:
        yield 1
        return
    for dir in DIRS:
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if 0 <= new_pos[0] < len(t_map) and 0 <= new_pos[1] < len(t_map[0]):
            if t_map[new_pos[0]][new_pos[1]][0] == val + 1 : # and t_map[new_pos[0]][new_pos[1]][1] == False:
                yield from check_adj(new_pos, val + 1, t_map)

def check_score(t_map: list, trailheads: list) -> int:
    """Returns the total score of all trailheads"""
    score = 0
    for start_pos in trailheads:
        """print("start pos:", start_pos)
        print("score:", sum(check_adj(start_pos, 0, copy_map(t_map))))"""
        score += sum(check_adj(start_pos, 0, copy_map(t_map)))
    return score

def main():
    t_map, trailheads = load_map(MAP_FILENAME)
    print("score:", check_score(t_map, trailheads))

if __name__ == "__main__":
    main()