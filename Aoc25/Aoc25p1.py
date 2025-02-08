"""
Advent of Code Day 25 part 1
Written by Trevor Ferris
2/7/2024
"""

"""Part 1 thoughts
struggling with finding a way to not iterate through the whole list of locks with each key might just make some slop and fix it after seeing part 2
THERE WASNT A PART TWO LOL"""

from time import time

LOCKS_FILENAME = "Aoc25/input.txt"
 
def load_locks(file_name: str) -> tuple[list[list[list[str]]], list[list[list[str]]]]:
    locks, keys = [], []
    with open(file_name, "r") as locks_file:
        for line in locks_file:
            if line[0] == "#":
                new_lock = []
                while line != ("\n"):
                    new_lock.append([ch for ch in line.rstrip("\n")])
                    line = locks_file.readline()
                    if not line:
                        break
                locks.append(new_lock)    
            else:
                new_key = []
                while line != ("\n"):
                    new_key.append([ch for ch in line.rstrip("\n")])
                    line = locks_file.readline()
                    if not line:
                        break
                keys.append(new_key)
    return locks, keys

def calc_height_map(pins: list[list[list[str]]], flipped: bool) -> list[list[int]]:
    """Builds a list of how high each column is for each key or lock in a given list
    
    Args:
        pins: 3D list of either keys or locks represented by a 2D list of .'s (Empty) and #'s (Filled) 
        
    Returns: A 2D list of keys or locks represented by a list of numbers corresponding to the height of filled spaces in that column"""

    height_maps = []
    for pin in pins:
        new_height_map = []
        for x in range(len(pin[0])):
            new_height_map.append(-1)
        for row in pin:
            for x in range(len(row)):
                if row[x] == "#":
                    new_height_map[x] += 1
        height_maps.append(new_height_map)
    if flipped:
        return flip_height(height_maps, len(pins[0]) - 2) # -2 because top and bottom rows are identifiers
    return height_maps

def flip_height(pin_heights, pin_len):
    fliped_pins = []
    for pin in pin_heights:
        fliped_pins.append([pin_len - v for v in pin])
    return fliped_pins

def sort_pins(pin_heights):
    sorted_heights = {}
    for i, pin_height in enumerate(pin_heights):
        sorted_heights[i] = "".join(str(h) for h in pin_height)
    return {k:str(v) for k,v in enumerate(sorted(sorted_heights.values()))}

def check_lock(lock, key):
    for x in range(len(key)):
        if key[x] > lock[x]:
            return False
    return True    
    
def find_keys(locks, keys):
    for key in keys.values():
        for lock in locks.values():
            if check_lock(lock, key):
                yield 1

def main():
    start_time = time()
    locks, keys = load_locks(LOCKS_FILENAME)
    lock_heights = sort_pins(calc_height_map(locks, True))
    key_heights = sort_pins(calc_height_map(keys, False))                           
    end_time = time()
    print(sum(find_keys(lock_heights, key_heights)))
    print(f"Time: {end_time - start_time}")
    
if __name__ == ("__main__"):
    main()