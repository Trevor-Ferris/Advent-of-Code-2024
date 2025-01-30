"""
Advent of code Problem 14 part 2
Written by Trevor Ferris
1/29/2025
"""

MOVEMENT_FILENAME = "input.txt"
B_WIDTH = 101
B_HEIGHT = 103

def load_movements(file_name: str) -> tuple[list[tuple[int]], list[tuple[int]]]:
    """Loads the starting positions and velocities of each robot from file"""
    positions, velocities = [], []
    with open(file_name, "r") as movements:
        for line in movements:    
            line = ''.join([x for x in line if not x.isalpha() and x not in ["=", "\n"]])
            pos, vel = line.split()
            p1, p2 = pos.split(",")
            v1, v2 = vel.split(",")
            positions.append((int(p1), int(p2)))
            velocities.append((int(v1), int(v2)))
    return positions, velocities

def print_map(pos: list[tuple[int]]):
    """Prints the map for debugging"""
    for y in range(B_HEIGHT):
        map_row = []
        for x in range(B_WIDTH):
            if num := pos.count((x, y)):
                map_row.append(num)
            else:
                map_row.append(".")
        print("".join(map(str, map_row)))

def check_dupe(new_pos: tuple[int]) -> bool:
    """checks the list of end positions for two stacked robots"""
    for pos in new_pos:
        if new_pos.count(pos) > 1:
            return False
    else:
        return True

def calc_pos(pos: tuple[int], vel: tuple[int], num_s: int) -> tuple[int]:
    """Calculates the position of a robot after a number of seconds"""
    return ((pos[0] + vel[0] * num_s) % B_WIDTH, (pos[1] + vel[1] * num_s) % B_HEIGHT)

def find_tree(pos: tuple[int], vel: tuple[int]) -> int:
    """Finds end positions the robots each second and checks if there are duplicates
        
        Returns: The number of seconds it took to find the first instance where the robots have no duplicates            
    """
    num_s = 0
    while True:
        end_pos = []
        for i in range(len(pos)):
            end_pos.append(calc_pos(pos[i], vel[i], num_s))
        if check_dupe(end_pos):
            print(num_s)
            return end_pos
        num_s += 1

def main():
    pos, vel = load_movements(MOVEMENT_FILENAME)
    print_map(find_tree(pos, vel))


if __name__ == ("__main__"):
    main()