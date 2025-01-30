"""
Advent of code Day 13 part 2
Written by Trevor Ferris
1/26/2025
Notes: I forgot linear algebra and needed help
"""

import math

PRIZE_FILENAME = "Aoc13/input.txt"
PRIZE_ERROR = 10000000000000

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

def calc_prizes(prizes, A_buttons, B_buttons):
    for i in range(len(prizes)):
        det_buttons = A_buttons[i][0] * B_buttons[i][1] - B_buttons[i][0] * A_buttons[i][1]
        det_b_p = prizes[i][0] * B_buttons[i][1] - B_buttons[i][0] * prizes[i][1]
        det_a_p = A_buttons[i][0] * prizes[i][1] - prizes[i][0] * A_buttons[i][1]      
        if det_a_p % det_buttons == 0 and det_b_p % det_buttons == 0:
            yield (3 * int(det_b_p / det_buttons) + int(det_a_p / det_buttons))
            
def main():
    prizes, A_buttons, B_buttons = load_prizes(PRIZE_FILENAME)  
    print("Tokens to win all prizes:", sum(calc_prizes(prizes, A_buttons, B_buttons)))

if __name__ == ("__main__"):
    main()