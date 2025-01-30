"""
Advent of Code day 4 problem 1
Written by Trevor Ferris
1/17/2025
"""

REPORTS_FILENAME = "Aoc4/input.txt"

def load_xword(file_name):
    inFile = open(file_name)
    xword = []
    for line in inFile:
        x_line = []
        line = line.replace('\n', '')
        for char in line:
            x_line.append(char)
        xword.append(x_line) 
    return xword

def check_opps(xword, pos1, pos2):
    xmas = "MS"
    if 0 < pos1 < len(xword) - 1 and 0 < pos2 < len(xword[pos1]) - 1:
        #Check if top right and left are m or s and then checks if the opposite corners are the reverse 
        #also lol
        if (xword[pos1 - 1][pos2 - 1] in xmas and 
            xword[pos1 + 1][pos2 + 1] == xmas.replace(xword[pos1 - 1][pos2 -1], "") and 
            xword[pos1 + 1][pos2 - 1] in xmas and 
            xword[pos1 - 1][pos2 + 1] == xmas.replace(xword[pos1 + 1][pos2 - 1], "")):
            return True
    return False

def xword_counter(xword):
    num_xmas = 0
    #iterate through all starting positions of a word
    for pos1 in range(len(xword)):
        for pos2 in range(len(xword[pos1])):
            if xword[pos1][pos2] == 'A':
                if check_opps(xword, pos1, pos2):
                    num_xmas += 1
    return num_xmas

if __name__ == ("__main__"):
    xword = load_xword(REPORTS_FILENAME)
    print ("Number of XMAS in crossword:", xword_counter(xword))
