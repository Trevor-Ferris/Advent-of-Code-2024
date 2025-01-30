"""
Advent of code day 11 problem 1
Written by Trevor Ferris
1/23/2025
"""

from time import time
from typing import Iterator

STONES_FILENAME = "input.txt"
NUM_BLINKS = 25

next_dict = {}

def load_stones(file_name: str) -> list[int]:
    """Loads the stones from a file"""
    with open(file_name, 'r') as stone_file:
        for stones in stone_file:
            return [int(x) for x in stones.split()]

def blink(stone: int) -> list:
    """Blinks the value of the stone and returns a list of the resulting stones"""
    if not next_dict.get(stone):
        if stone == 0:
            next_dict[stone] = [1]
        elif not len(stone_str := str(stone)) % 2:
            stone1, stone2 = stone_str[:int(len(stone_str) / 2)], stone_str[int(len(stone_str) / 2):]
            next_dict[stone] = [int(stone1), int(stone2)]
        else:
            next_dict[stone] = [stone * 2024]
    return next_dict[stone]
        
def run_blinks(stones: list) -> int:
    """Runs the blink function a number of times and returns the resulting number of stones"""
    
    for x in range(NUM_BLINKS):
        new_stones = []
        for stone in stones:
            new_stones.extend(blink(stone))
        stones = new_stones
    return len(stones)

def main():
    start_time = time()
    stones = load_stones(STONES_FILENAME)
    print(run_blinks(stones))
    end_time = time()
    print(f"Run time: {end_time - start_time}")

if __name__ == "__main__":
    main()