"""
Advent of Code day 21 part 1
Written by Trevor Ferris
2/4/2025
Notes: rough
"""

from enum import StrEnum
from typing import Iterator
from time import time

CODES_FILENAME = "Aoc21/input.txt"
INNER_BUTTON = "Aoc21/inner_button.txt"
OUTER_BUTTON = "Aoc21/outer_button.txt"
NUM_OUTER_KEYPADS = 3
INNER_VALS = " 0A123456789"
OUTER_VALS = "<v> ^A"
DIRS = ["<","^", "v", ">"]

class Buttons(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    ENTER = "A"
    NULL = " "

def load_codes(file_name: str) -> list[list[str]]:
    codes = []
    with open(file_name, "r") as codes_file:
        for line in codes_file:
            line = line.rstrip("\n")
            code = [ch for ch in line]
            codes.append(code)
    return codes
   
def build_button(file_name: str) -> list[list[str]]:
    buttons = []
    with open(file_name, "r") as buttons_file:
        for line in buttons_file:
            line = line.rstrip("\n")
            button_row = [ch for ch in line]
            buttons.append(button_row)
    return buttons

def dir_check(dir: tuple) -> tuple[int, int]:
    """Gives coordinate movement of given direction"""
    match dir:
        case (1, 0):
            return Buttons.UP.value
        case (-1, 0):
            return Buttons.DOWN.value
        case (0, -1):
            return Buttons.RIGHT.value
        case (0, 1):
            return Buttons.LEFT.value

def find_fastest_path(buttons: list[list[str]], button_vals: str, start: str, tar: str) -> list[str]:
    """Finds the fastest path between the start and the target
    
    In order to find the fastest path: First, the path must be as straight as possible in order to allow the robot to press the same button in succession if possible
    Then, if possible the path must place the arrows in the prioritizing the further away arrows on the pad
    Therefore for the given keypad 1) "<", (0, -1) | 2) "v" (-1, 0) | 3) ">", "^" is the priority as long as the moves do not place it over the hole at any point
    
    Args:
        buttons: 2D list containing the keypad
        button_vals: string containing the values of the keypad
        start: The value to path from
        tar: The value to path to

    Returns:
        The fastest path from start to tar given as arrows (><v^) terminated by A
    """
    
    path = []
    #find the coordinates of the two buttons in the lists 
    start_pos = (len(buttons) - (button_vals.index(start) // len(buttons[0]) + 1), 
                 button_vals.index(start) % len(buttons[0]))
    end_pos = (len(buttons) - (button_vals.index(tar) // len(buttons[0]) + 1), 
               button_vals.index(tar) % len(buttons[0]))
    diff_x, diff_y = start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]
    if buttons[start_pos[0]][start_pos[1] - diff_y] == " ":
        for x in range(abs(diff_x)):
            path.append(dir_check((diff_x / abs(diff_x), 0)))
        for y in range(abs(diff_y)):
            path.append(dir_check((0, diff_y / abs(diff_y))))
    elif buttons[start_pos[0] - diff_x][start_pos[1]] == " ":
        for y in range(abs(diff_y)):
            path.append(dir_check((0, diff_y / abs(diff_y))))
        for x in range(abs(diff_x)):
            path.append(dir_check((diff_x / abs(diff_x), 0)))
    else:
        if diff_y > 0:
            for y in range(abs(diff_y)):
                path.append(dir_check((0, diff_y / abs(diff_y))))
        if diff_x > 0:
            for x in range(abs(diff_x)):
                path.append(dir_check((diff_x / abs(diff_x), 0)))
        if diff_x < 0:
            for x in range(abs(diff_x)):
                path.append(dir_check((diff_x / abs(diff_x), 0)))
        if diff_y < 0:
            for y in range(abs(diff_y)):
                path.append(dir_check((0, diff_y / abs(diff_y))))
    path.append(Buttons.ENTER.value)
    return path
            
def build_button_dict(buttons: list[list[str]], button_vals: str) -> dict[str: str]:
    """Builds a dictionary of each button and the sequences of directions to reach each button from there"""
    button_dict = {}
    for x, row in enumerate(buttons):
        for y, val in enumerate(row):    
            if val == Buttons.NULL:
                continue
            button_dict[val] = []                  
            for tar in button_vals:
                if tar == Buttons.NULL:
                    button_dict[val].append("BLANK")
                    continue
                button_dict[val].append(find_fastest_path(buttons, button_vals, val, tar))
    return button_dict

def calc_outer_codes(code: str, inner_dict: dict[str: str], outer_dict: dict[str: str]) -> str:    
    #Set robot starting positions
    robot_pos = [Buttons.ENTER.value for x in range(NUM_OUTER_KEYPADS + 2)]
    total_buttons = []
    #iterate through each value in the code
    for inner in code:
        #make a list of the moves this robot needs to take to reach the value
        button_list = (inner_dict[robot_pos[0]][INNER_VALS.index(inner)])
        #move the robot to the position 
        robot_pos[0] = inner
        #iterate through the list a number of times equal to the number of keypads
        for x in range(NUM_OUTER_KEYPADS - 1):
            new_button_list = []
            for outer in button_list:
                #add the list of moves needed to a new list
                new_button_list.extend(outer_dict[robot_pos[x + 1]][OUTER_VALS.index(outer)])
                #move the robot to the position
                robot_pos[x + 1] = outer
            #make the button list equal to the new button list
            button_list = new_button_list
        #add the list to the total buttons and move to the next value
        total_buttons.extend(button_list)
    #print (code, ":", "".join(total_buttons))
    return total_buttons

def calc_complexity(codes: str, inner_dict: dict[str: str], outer_dict: dict[str: str]) -> Iterator[int]:
    """Calculates the complexity score of a list of codes"""
    for code in codes:       
        print("...")
        yield int("".join(ch for ch in code if ch.isnumeric())) * len(calc_outer_codes(code, inner_dict, outer_dict))

def main():
    start_time = time()
    codes = load_codes(CODES_FILENAME)
    inner_dict = build_button_dict(build_button(INNER_BUTTON), INNER_VALS)
    outer_dict = build_button_dict(build_button(OUTER_BUTTON), OUTER_VALS)   
    print(sum(calc_complexity(codes, inner_dict, outer_dict)))
    end_time = time()
    print(f"Time elapsed{end_time - start_time}")

if __name__ == ("__main__"):
    main()