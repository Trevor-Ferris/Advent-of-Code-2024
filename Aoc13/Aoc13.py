"""
Advent of code Day 13 part 1
Written by Trevor Ferris
1/26/2025
Notes: Runs slower than p2 even with no error but here for posterity
"""

PRIZE_FILENAME = "Aoc13/input.txt"

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
                prizes.append(((int(line[line.find("X=") + 2 :line.find(",")])), 
                                  (int(line[line.find("Y=") + 2:]))))
                continue
    return prizes, A_buttons, B_buttons

def check_button(prize, A_button, B_button):
    for a in range(1, 100):
        for b in range(1, 100):
            if A_button[0] * a + B_button[0] * b == prize[0] and A_button[1] * a + B_button[1] * b == prize[1]:
                return (a, b)
    return(None, None)

def calc_prizes(prizes, A_buttons, B_buttons):
    for index, prize in enumerate(prizes):
        num_a, num_b = (check_button(prize, A_buttons[index], B_buttons[index]))
        if num_a:    
            yield (num_a * 3 + num_b)
            
def main():
    prizes, A_buttons, B_buttons = load_prizes(PRIZE_FILENAME)
    print("Tokens to win all prizes:", sum(calc_prizes(prizes, A_buttons, B_buttons)))

if __name__ == ("__main__"):
    main()