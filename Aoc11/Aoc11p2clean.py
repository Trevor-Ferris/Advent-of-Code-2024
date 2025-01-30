"""
Advent of code day 11 problem 2
Written by Trevor Ferris
1/23/2025
"""

from time import time
from typing import Iterator

STONES_FILENAME = "input.txt"
NUM_BLINKS = 125

def load_stones(file_name: str) -> list[int]:
    """Loads the stones from a file"""
    with open(file_name, 'r') as stone_file:
        for stones in stone_file:
            return [int(x) for x in stones.split()] 
 
def blink(stone: int, num_blinks: int, start_blink: int, blink_dict: dict) -> int:
    """
    Calculates the number of stones after a given number of blinks

    Args:
        stone: Value of the stone
        num_blinks: Blinks remaining
        start_blinks: Number of blinks to check from the start, primarily used to quickly check if the value is in the dictionary
        blink_dict: Dictionary containing stone values keyed to the number of resulting stones after a number of blinks

    Returns:
        The number of stones resulting from a number of blinks on the initial stone
    """
    if num_blinks == 0:
        return 1
    elif stone < 10 and num_blinks < start_blink:
        return blink_dict[stone][num_blinks]  
    elif not len(stone_str := str(stone)) % 2:
        stone1, stone2 = stone_str[:int(len(stone_str) / 2)], stone_str[int(len(stone_str) / 2):]
        return (blink(int(stone1), num_blinks - 1, start_blink, blink_dict) + 
                blink(int(stone2), num_blinks - 1, start_blink, blink_dict))
    elif stone == 0:
        return blink(1, num_blinks - 1, start_blink, blink_dict)
    else:
        return blink(stone * 2024, num_blinks - 1, start_blink, blink_dict)        

def build_blink_dict() -> dict:
    """Builds a dictionary containing the number of stones resulting from 0 to the number of blinks desired"""
    blink_dict = {}
    for x in range(10):
        blink_dict[x] = []
    for x in range(NUM_BLINKS + 1):
        for y in range(10):
            blink_dict[y].append(blink(y, x, x, blink_dict))
    return blink_dict
  
def run_blinks(stones: list, blink_dict: dict) -> Iterator[int]:
    """Runs the blink function on each stone in the given input"""
    for stone in stones:
        yield blink(stone, NUM_BLINKS, NUM_BLINKS, blink_dict)               

def main():
    start_time = time()
    stones = load_stones(STONES_FILENAME)   
    print(sum(run_blinks(stones, build_blink_dict())))
    end_time = time()
    print(f"Run time: {end_time - start_time}")

if __name__ == "__main__":
    main()