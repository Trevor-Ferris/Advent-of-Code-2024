"""
Advent of code Problem 14 part 1
Written by Trevor Ferris
1/29/2025
"""

MOVEMENT_FILENAME = "Aoc14/input.txt"
NUM_SECONDS = 100
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

def calc_pos(pos: tuple[int], vel: tuple[int]) -> int:
    """Calculates the position of a robot after a number of seconds"""
    return ((pos[0] + vel[0] * NUM_SECONDS) % B_WIDTH, (pos[1] + vel[1] * NUM_SECONDS) % B_HEIGHT)

def calc_end_pos(pos: list[tuple[int]], vel: list[tuple[int]]) -> list:
    """Calculates the of end positions of each robot after a number of seconds"""
    end_pos = []
    for i in range(len(pos)):
        end_pos.append(calc_pos(pos[i], vel[i]))
    return end_pos

def calc_safety(end_pos: list[tuple[int]]) -> int:
    """Calculates the safety score of a given list of end positions"""
    q1, q2, q3, q4 = 0, 0, 0, 0
    for pos in end_pos:
        if pos[0] > (B_WIDTH - 1) / 2:
            if pos[1] > (B_HEIGHT - 1) / 2:
                q1 += 1
            elif pos[1] < (B_HEIGHT - 1) / 2:
                q2 += 1
        elif pos[0] < (B_WIDTH - 1) / 2:
            if pos[1] > (B_HEIGHT - 1) / 2:
                q3 += 1
            elif pos[1] < (B_HEIGHT - 1) / 2:
                q4 += 1
    return q1 * q2 * q3 * q4

def main():
    pos, vel = load_movements(MOVEMENT_FILENAME)
    end_pos = calc_end_pos(pos, vel)
    print("Safety score:", calc_safety(end_pos))

if __name__ == ("__main__"):
    main()
            