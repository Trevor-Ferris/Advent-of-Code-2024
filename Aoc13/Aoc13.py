"""
Advent of code Day 13 problem 1
Written by Trevor Ferris
1/26/2025
"""

import math

PRIZE_FILENAME = "input.txt"
PRIZE_ERROR = 10000000000000
#PRIZE_ERROR = 0


def load_prizes(file_name):
    prizes, A_buttons, B_buttons = [], [], []    
    with open(file_name, "r") as prize_file:
        for line in prize_file:
            line.rstrip("\n")
            if "A" in line:
                A_buttons.append((int(line[line.find("X+") + 2 :line.find(",")]), 
                                  int(line[line.find("Y+") + 2:])))
                continue
            if "B" in line:
                B_buttons.append((int(line[line.find("X+") + 2 :line.find(",")]), 
                                  int(line[line.find("Y+") + 2:])))
                continue
            if "P" in line:
                prizes.append(((int(line[line.find("X=") + 2 :line.find(",")]) + PRIZE_ERROR), 
                                  (int(line[line.find("Y=") + 2:])) + PRIZE_ERROR))
                continue
    return prizes, A_buttons, B_buttons

def jiggle(prize, A_button, B_button, num_a, num_b):
    print(num_a, num_b)
    for a in range(num_a - 1000, num_a + 1000):
        for b in range(num_b - 100, num_b + 100):
            if A_button[0] * a + B_button[0] * b == prize[0] and A_button[1] * a + B_button[1] * b == prize[1]:
                return (a, b)
    return(None, None)

def bis_search(prize, A_button, B_button):
    prev_a_low, prev_a_high = 0, math.ceil(prize[0] / A_button[0])
    prev_b_low, prev_b_high = 0, math.ceil(prize[0] / B_button[0]) 
    curr_a = int((prev_a_low + prev_a_high) / 2)
    curr_b = int((prev_b_low + prev_b_high) / 2)
    A_y_high = A_button[1] > B_button[1]
    while curr_a not in (prev_a_high, prev_a_low) and curr_b not in (prev_b_high, prev_b_low):
        tot_y = curr_a * A_button[1] + curr_b * B_button[1]
        if tot_y > prize[1]:
            if A_y_high:
                curr_a, prev_a_high = int((curr_a + prev_a_low) / 2), curr_a
                curr_b, prev_b_low = int((curr_b + prev_b_high) / 2), curr_b
            else:
                curr_a, prev_a_low = int((curr_a + prev_a_high) / 2), curr_a
                curr_b, prev_b_high = int((curr_b + prev_b_low) / 2), curr_b
        else:
            if A_y_high:
                curr_a, prev_a_low = int((curr_a + prev_a_high) / 2), curr_a
                curr_b, prev_b_high = int((curr_b + prev_b_low) / 2), curr_b                
            else:
                curr_a, prev_a_high = int((curr_a + prev_a_low) / 2), curr_a
                curr_b, prev_b_low = int((curr_b + prev_b_high) / 2), curr_b
    return (curr_a, curr_b)


def calc_prizes(prizes, A_buttons, B_buttons):
    for index, prize in enumerate(prizes):
        j_a, j_b = bis_search(prize, A_buttons[index], B_buttons[index])
        num_a, num_b = (jiggle(prize, A_buttons[index], B_buttons[index],j_a, j_b))
        if num_a:    
            yield (num_a * 3 + num_b)
            

        

def main():
    prizes, A_buttons, B_buttons = load_prizes(PRIZE_FILENAME)
    
    print(sum(calc_prizes(prizes, A_buttons, B_buttons)))

if __name__ == ("__main__"):
    main()