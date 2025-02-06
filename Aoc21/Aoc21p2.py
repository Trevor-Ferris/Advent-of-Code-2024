"""
Advent of Code day 21 part 2
Written by Trevor Ferris
2/4/2025
Notes: Super happy with how fast it runs, not super happy about some of the implementations
In retrospect I think the path finding was a bit too manual and could potentially have been done through the second order outer keypad
Also at one point in testing I made python use 13GB of RAM so that was fun
"""

from enum import StrEnum
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

def find_fastest_path(buttons: list[list[str]], button_vals, start, tar: str):
    """Finds the straightest path between the start and the target"""
    path = []
    #find the coordinates of the two buttons in the lists 
    start_pos = (len(buttons) - (button_vals.index(start) // len(buttons[0]) + 1), 
                 button_vals.index(start) % len(buttons[0]))
    end_pos = (len(buttons) - (button_vals.index(tar) // len(buttons[0]) + 1), 
               button_vals.index(tar) % len(buttons[0]))
    #find the number of x movements (up(-) and down(+)) and y movements(left(-) and right(+))
    diff_x, diff_y = start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]
    """                                            INPUT PRIORITY 
    First, the path must be as straight as possible in order to allow the robot to press the same button in succession if possible
    Then, if possible the path must place the arrows in the prioritizing the further away arrows on the pad
    Therefore for the given keypad 1) "<", (0, -1) | 2) "v" (-1, 0) | 3) ">", "^" is the priority as long as the moves do not place it over the hole at any point"""
    #check if the whole "<" move would put it in the hole. If the movement would put it into a hole then the vertical movement must be ^ 
    if buttons[start_pos[0]][start_pos[1] - diff_y] == " ":
        #append the vertical move and then the horizontal
        for x in range(abs(diff_x)):
            path.append(dir_check((diff_x / abs(diff_x), 0)))
        for y in range(abs(diff_y)):
            path.append(dir_check((0, diff_y / abs(diff_y))))
    #check if the whole "v" move would put it into the hole. Similar to above if so then the horizontal must be >
    elif buttons[start_pos[0] - diff_x][start_pos[1]] == " ":
        #append the horizontal move and then the vertical move
        for y in range(abs(diff_y)):
            path.append(dir_check((0, diff_y / abs(diff_y))))
        for x in range(abs(diff_x)):
            path.append(dir_check((diff_x / abs(diff_x), 0)))
    #the movement at this point will not go into a hole and can go by priority
    else:
        #check for any < movement
        if diff_y > 0:
            for y in range(abs(diff_y)):
                path.append(dir_check((0, diff_y / abs(diff_y))))
        #check for any v movement
        if diff_x > 0:
            for x in range(abs(diff_x)):
                path.append(dir_check((diff_x / abs(diff_x), 0)))
        #who gives a fuck
        if diff_x < 0:
            for x in range(abs(diff_x)):
                path.append(dir_check((diff_x / abs(diff_x), 0)))
        if diff_y < 0:
            for y in range(abs(diff_y)):
                path.append(dir_check((0, diff_y / abs(diff_y))))
    path.append(Buttons.ENTER.value)
    return "".join(path)
            
def build_button_dict(buttons: list[list[str]], button_vals) -> dict[str: str]:
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

def build_deep_dict(button_dict):
    "Builds a dictionary of multiple order outer button presses"
    #Build a set containing each possible button code
    all_dir_codes = set()
    for vals in button_dict.values():
        for val in vals:
            if val != "BLANK":
                all_dir_codes.add("".join(ch for ch in val))
    #Build a dictionary containing each of those values keyed to a list of strings containing the value after list index number of buttons
    deep_dict = {val: [len(val)] for val in all_dir_codes}
    #Iterate through each value in the dictionary a number of times equal to the outer keypads
    for x in range(1, NUM_OUTER_KEYPADS):
        for code in deep_dict:
            #For each code find the next next code and then divide the code into individual button presses
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
            #The dict contains all used button combinations up to x - 1, since the previous step used one keypad each button resulting is in the dict
            for button in button_presses:
                code_len += deep_dict[button][x - 1]
            #append the sum of the buttons to the end of the list
            deep_dict[code].append(code_len)
    return deep_dict

def calc_outer_codes(code, inner_dict, outer_dict, deep_dict):
    """Calculates the length of a code from the number of keypads"""
    robot_pos = Buttons.ENTER.value
    end_code = 0
    for inner in code:
        #Make a list of the moves the inner robot takes
        button_list = (inner_dict[robot_pos][INNER_VALS.index(inner)])
        #Move the robot to the position for the next code 
        robot_pos = inner
        #Generate the initial list of moves on the first outer keypad
        robot_pos2 = Buttons.ENTER.value
        new_button_list = []
        for outer in button_list:
            #Add the list of moves needed to a new list
            new_button_list.extend(outer_dict[robot_pos2][OUTER_VALS.index(outer)])
            #Move the robot to the position
            robot_pos2 = outer
        #Break the button into whole button inputs and add the lengths together 
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

def calc_complexity(codes, inner_dict, outer_dict, deep_dict):
    """Calculates the complexity score of a list of codes"""
    for code in codes:       
        yield int("".join(ch for ch in code if ch.isnumeric())) * calc_outer_codes(code, inner_dict, outer_dict, deep_dict)

def main():
    start_time = time()
    codes = load_codes(CODES_FILENAME)
    inner_dict = build_button_dict(build_button(INNER_BUTTON), INNER_VALS)
    outer_dict = build_button_dict(build_button(OUTER_BUTTON), OUTER_VALS)   
    deep_dict = build_deep_dict(outer_dict)
    print(sum(calc_complexity(codes, inner_dict, outer_dict, deep_dict)))
    end_time = time()
    print(f"Time elapsed{end_time - start_time}")

if __name__ == ("__main__"):
    main()