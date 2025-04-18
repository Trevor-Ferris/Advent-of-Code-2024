"""
Advent of code day 11 part 2
Written by Trevor Ferris
1/23/2025
Notes: Twice as fast but looks less readable
"""

from time import time
from typing import Iterator

STONES_FILENAME = "Aoc11/input.txt"
NUM_BLINKS = 75

next_dict = {}

def load_stones(file_name: str) -> list[int]:
    """Loads the stones from a file"""
    with open(file_name, 'r') as stone_file:
        for stones in stone_file:
            return [int(x) for x in stones.split()] 

def blink_dict_help(stone, num_blinks, start_blink, blink_dict):
    if num_blinks == 0:
        return 1
    if stone < 10 and num_blinks < start_blink:
        return blink_dict[stone][num_blinks]
    if not next_dict.get(stone):
        if stone == 0:
            next_dict[stone] = [1]
        elif not len(stone_str := str(stone)) % 2:
            stone1, stone2 = stone_str[:int(len(stone_str) / 2)], stone_str[int(len(stone_str) / 2):]
            next_dict[stone] = [int(stone1), int(stone2)]
        else:
            next_dict[stone] = [stone * 2024]        
    new_stones = 0
    for s_stone in next_dict[stone]:                        
        new_stones += blink_dict_help(s_stone, num_blinks - 1, start_blink, blink_dict)
    return new_stones

def build_blink_dict():
    blink_dict = {}
    for x in range(10):
        blink_dict[x] = []
    for x in range(NUM_BLINKS + 1):
        for y in range(10):
            blink_dict[y].append(blink_dict_help(y, x, x, blink_dict))
    return blink_dict

def blink_with_dict(stone: int, num_blinks: int, blink_dict: dict) -> list:
    new_stones = 0
    if num_blinks == 0:
        return 1     
    if stone < 10:
        return blink_dict[stone][num_blinks]   
    if not next_dict.get(stone):
        if stone == 0:
            next_dict[stone] = [1]
        elif not len(stone_str := str(stone)) % 2:
            stone1, stone2 = stone_str[:int(len(stone_str) / 2)], stone_str[int(len(stone_str) / 2):]
            next_dict[stone] = [int(stone1), int(stone2)]
        else:
            next_dict[stone] = [stone * 2024]        
    for s_stone in next_dict[stone]:                        
        new_stones += blink_with_dict(s_stone, num_blinks - 1, blink_dict)
    return new_stones
   
def run_blinks(stones: list, blink_dict: dict) -> Iterator[int]:
    """Runs the blink function a number of times and returns the resulting number of stones"""
    for stone in stones:
        yield blink_with_dict(stone, NUM_BLINKS, blink_dict)

def main():
    start_time = time()
    stones = load_stones(STONES_FILENAME)   
    print("Number of stones after", NUM_BLINKS, "blinks:", sum(run_blinks(stones, build_blink_dict())))
    end_time = time()
    print(f"Run time: {end_time - start_time}")

if __name__ == "__main__":
    main()