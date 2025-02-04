"""
Advent of Code day 19 part 1
Written by Trevor Ferris
2/3/2025
"""

from time import time
TOWELS_FILENAME = "Aoc19/input.txt"

def load_towels(file_name: str) -> tuple[list[str], list[str]]:
    """Load list of towels and displays from file"""
    displays = []
    with open(file_name, "r") as towel_file:
        towels_file = towel_file.readline()
        towels_file = towels_file.rstrip("\n")
        towels = towels_file.split(", ")
        towel_file.readline()
        for display in towel_file:
            display = display.rstrip("\n")
            displays.append(display)
    return towels, displays 

def check_display(towels, display, long_towel):
    """Returns true if the display can be made from any combination of towels"""
    if display in towels:
        return True
    for pos in range(1, len(display)):
        if display[:pos] in towels:
            return check_display(towels, display[pos:], long_towel)
        if pos > long_towel:
            return False
    return False

def find_num_displays(towels, displays):
    """Returns the total number of valid displays"""
    long_towel = max([len(towel) for towel in towels])
    for display in displays:
        if check_display(towels, display, long_towel):
            yield 1

def main():
    start_time = time()
    towels, displays = load_towels(TOWELS_FILENAME)
    print(f"Number of valid displays: {sum(find_num_displays(towels, displays))}")
    end_time = time()
    print(f"Time: {end_time - start_time}")
    
if __name__ == ("__main__"):
    main()