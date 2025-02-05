"""
Advent of Code day 21 part 1
Written by Trevor Ferris
2/4/2025
Notes: rough
"""

from enum import StrEnum
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
    return path
            
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

def calc_outer_codes(code, inner_dict, outer_dict):    
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
    print(code, ":", "".join(str(ch) for ch in total_buttons), len(total_buttons))
    return total_buttons

def calc_complexity(codes, inner_dict, outer_dict):
    """Calculates the complexity score of a list of codes"""
    for code in codes:       
        yield int("".join(ch for ch in code if ch.isnumeric())) * len(calc_outer_codes(code, inner_dict, outer_dict))

def main():
    start_time = time()
    codes = load_codes(CODES_FILENAME)
    inner_dict = build_button_dict(build_button(INNER_BUTTON), INNER_VALS)
    outer_dict = build_button_dict(build_button(OUTER_BUTTON), OUTER_VALS)   
    print(sum(calc_complexity(codes, inner_dict, outer_dict)))
    end_time = time()
    print(f"Time elapsed{end_time - start_time}")
    """for key, vals in inner_dict.items():
        for i, val in enumerate(vals):
            print (f"{key} to {INNER_VALS[i]} path: {val}")
    for key, vals in outer_dict.items():
        for i, val in enumerate(vals):
            print (f"{key} to {OUTER_VALS[i]} path: {val}")"""

if __name__ == ("__main__"):
    main()