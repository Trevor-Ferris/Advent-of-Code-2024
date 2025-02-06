"""
Advent of Code day 21 part 2
Written by Trevor Ferris
2/4/2025
Notes: Super happy with how fast it runs, not super happy about some of the implementations
In retrospect I think the path finding was a bit too manual and could potentially have been done through the second order outer keypad
Also at one point in testing I made python use 13GB of RAM so that was fun
"""

from enum import StrEnum
from typing import Iterator
from time import time

CODES_FILENAME = "Aoc21/input.txt"
INNER_BUTTON = "Aoc21/inner_button.txt"
OUTER_BUTTON = "Aoc21/outer_button.txt"
NUM_OUTER_KEYPADS = 25
INNER_VALS = " 0A123456789"
OUTER_VALS = "<v> ^A"

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
    match dir:
        case (1, 0):
            return Buttons.UP.value
        case (-1, 0):
            return Buttons.DOWN.value
        case (0, -1):
            return Buttons.RIGHT.value
        case (0, 1):
            return Buttons.LEFT.value

def find_fastest_path(buttons: list[list[str]], button_vals: str, start: str, tar: str) -> str:
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
    return "".join(path)
            
def build_button_dict(buttons: list[list[str]], button_vals: str) -> dict[str: str]:
    """Builds a dictionary of each button and the sequences of directions to reach each button from there
    
    Args: 
        buttons: 2D list containing the buttons on the keypad
        button_vals: string containing each value in the keypad

    Returns:
        A dictionary containing the fastest path from each button in the keyboard to each button in the keyboard
    """
    
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

def build_deep_dict(button_dict: dict[str: str]) -> dict[str: int]:
    """Builds a dictionary of multiple order outer button presses
    
    For each possible sequence of a button press (arrows terminated by "A") calculate the number of instructions 
    that the string is at any value up to the number of outer keypads. Store the value in a dict {path: list[path length]}
    Since the dict contains all used sequences it can be used to further build the dictionary quickly

    Args:
        button_dict: dictionary containing the optimal paths from any button to the next

    Returns:
        A dictionary containing the resulting length of the sequence of buttons after a number of outer buttons (path: length) 
    """

    all_dir_codes = set()
    for vals in button_dict.values():
        for val in vals:
            if val != "BLANK":
                all_dir_codes.add("".join(ch for ch in val))
    deep_dict = {val: [len(val)] for val in all_dir_codes}
    for x in range(1, NUM_OUTER_KEYPADS):
        for code in deep_dict:
            button_presses = []
            code_len = 0
            new_button = ""
            r_pos = Buttons.ENTER.value
            for input in code:
                new_button += button_dict[r_pos][OUTER_VALS.index(input)]
                r_pos = input
            while Buttons.ENTER in new_button:
                button_presses.append(new_button[:new_button.index(Buttons.ENTER) + 1])
                new_button = new_button[new_button.index(Buttons.ENTER) + 1:]
            for button in button_presses:
                code_len += deep_dict[button][x - 1]
            deep_dict[code].append(code_len)
    return deep_dict

def calc_outer_codes(code: str, inner_dict: dict[str: str] , outer_dict: dict[str: str], deep_dict: dict[str: int]) -> int:
    """Calculates the length of a code from the number of keypads
    
    For each button the inner robot needs to hit get the sequence from the inner dict 
    using that find the sequence the first outer robot needs to move 
    for each full button press find the resulting number of buttons from the deep dict

    Args:
        code: The sequence the inner robot needs to press ie. (029A)
        inner_dict: Dictionary containing the fastest path from any 2 inner buttons to another (start value: path)
        outer_dict: Dictionary containing the fastest path from any 2 outer buttons to another (start value: path)
        deep_dict: Dictionary containing the resulting length of the sequence of buttons after a number of outer buttons (path: length)

    Returns:
        The length of the input being pressed on the last keypad
    """

    robot_pos = Buttons.ENTER.value
    end_code = 0
    for inner in code:
        button_list = (inner_dict[robot_pos][INNER_VALS.index(inner)]) 
        robot_pos = inner
        robot_pos2 = Buttons.ENTER.value
        new_button_list = []
        for outer in button_list:
            new_button_list.extend(outer_dict[robot_pos2][OUTER_VALS.index(outer)])
            robot_pos2 = outer 
        code_copy = "".join(new_button_list)
        button_presses = []
        while Buttons.ENTER in code_copy:
            button_presses.append(code_copy[:code_copy.index(Buttons.ENTER) + 1])
            code_copy = code_copy[code_copy.index(Buttons.ENTER) + 1:]
        outer_code = 0
        for button in button_presses:
            outer_code += deep_dict[button][NUM_OUTER_KEYPADS - 1]
        end_code += outer_code
    return end_code

def calc_complexity(codes: str, inner_dict: dict[str: str], outer_dict: dict[str: str], deep_dict: dict[str: int]) -> Iterator[int]:    
    for code in codes:       
        yield int("".join(ch for ch in code if ch.isnumeric())) * calc_outer_codes(code, inner_dict, outer_dict, deep_dict)

def main():
    start_time = time()
    codes = load_codes(CODES_FILENAME)
    inner_dict = build_button_dict(build_button(INNER_BUTTON), INNER_VALS)
    outer_dict = build_button_dict(build_button(OUTER_BUTTON), OUTER_VALS)   
    deep_dict = build_deep_dict(outer_dict)
    print(f"Complexity score: {sum(calc_complexity(codes, inner_dict, outer_dict, deep_dict))}")
    end_time = time()
    print(f"Time elapsed{end_time - start_time}")

if __name__ == ("__main__"):
    main()