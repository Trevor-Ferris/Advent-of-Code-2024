"""
Advent of Code day 19 part 2
Written by Trevor Ferris
2/3/2025
Notes: Off by one hell
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

def calc_permutations(towels: list[str], display: str, long_towel: int) -> int:
    """
    Runs through the display in reverse and adds the number of permutations at that point to a dict
    
    Args:
        towels: the list of towels
        display: the current display string
        long_towel: the length of the longest towel

    Returns: The number of permutations of towels that can make the display
    """
    pos_dict = {}
    for i in range(-1, - len(display) - 1, -1):
        num_perm = 0
        #If the entirety of the section of display is able to be 
        #made with a single towel add a permutation to this section
        if display[i:] in towels:
            num_perm += 1
        j = i + 1    
        #Run through possible sections (Shorter than the longest towel and not longer than the whole section)
        while j < i + long_towel + 1 and j < 0:
            #If the section can fit in the display then find the number of permutations of 
            #the remaining section and add it to this section
            if display[i:j] in towels:
                num_perm += pos_dict[j]
            j += 1
        pos_dict[i] = num_perm
    return pos_dict[- len(display)]    

def find_num_displays(towels, displays):
    """Finds the number of permutations for each display"""
    long_towel = max([len(towel) for towel in towels])
    for display in displays:
        yield calc_permutations(towels, display, long_towel)

def main():
    start_time = time()
    towels, displays = load_towels(TOWELS_FILENAME)
    print(f"Number of valid permutations: {sum(find_num_displays(towels, displays))}")
    end_time = time()
    print(f"Time: {end_time - start_time}")
    
if __name__ == ("__main__"):
    main()