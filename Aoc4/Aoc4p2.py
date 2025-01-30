#Advent of Code day 4 problem 2
#Made by Trevor Ferris
#1/17/2025

REPORTS_FILENAME = "Documents\Python Practice\Aoc4\input.txt"

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

def check_next(xword, xletter, pos1, pos2, dir1, dir2):
    xmas = "XMAS"
    if xletter == 'S':
        return True
    if pos1 + dir1 in range(len(xword)): 
        if pos2 + dir2 in range(len(xword[pos1 + dir1])):
            if xword[pos1 + dir1][pos2 + dir2] == xmas[xmas.find(xletter) + 1]:
                pos1 += dir1
                pos2 += dir2
                return check_next(xword, xword[pos1][pos2], pos1, pos2, dir1, dir2) 
    return False

def xword_counter(xword):
    num_xmas = 0
    #iterate through all starting positions of a word
    print (xword)
    for pos1 in range(len(xword)):
        for pos2 in range(len(xword[pos1])):
            if xword[pos1][pos2] == 'A':
                #iterate through all directions a word can start
                for dir1 in range(-1, 2, ):
                    for dir2 in range(-1, 2,):
                        print (dir1, dir2)
                        if check_next(xword, xword[pos1][pos2], pos1, pos2, dir1, dir2):
                            num_xmas +=1

    return num_xmas


if __name__ == ("__main__"):
    xword = load_xword(REPORTS_FILENAME)
    print (xword_counter(xword))
