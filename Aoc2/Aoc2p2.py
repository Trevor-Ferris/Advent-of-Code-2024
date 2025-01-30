"""
Advent of Code day 2 part 2
Written by Trevor Ferris
1/14/2025
Notes: Part 1 is lost
"""

REPORTS_FILENAME = "Aoc2/input.txt"

def load_reports(file_name):
    inFile = open(file_name, 'r')
    reports = []
    for line in inFile:
        reports.append(list(map(int, line.split())))
    return reports

def seq_check(levels, position, rising, dampener):
    #Check if all the levels have been checked and returns True if so
    if position == len(levels):
        return True
    #if the change is more than 3 return trigger the dampener or return false if already done so
    if (abs(levels[position - 1]-levels[position]) <= 3):
    #if the next level is in the same direction as before then recursively call either until it is not or until it is the last position
        if (levels[position - 1] < levels[position]) and rising:
            return seq_check(levels, (position + 1), rising, dampener)
        elif (levels[position - 1] > levels[position])  and not rising:
            return seq_check(levels, (position+  1), rising, dampener)
    #dampener checks if levels works either without the current level or the previous level with the dampener set to false
    if dampener:
        levels_copy = levels.copy()
        if (position - 1) >= 0:
            levels_copy.pop(position - 1)
            if seq_check(levels_copy, 1 , rising, False):
                return True
        levels_copy = levels.copy()
        levels_copy.pop(position)
        if seq_check(levels_copy, 1, rising, False):
            return True
    return False

def safe_check(reports):
    num_safe = 0
    for levels in reports:
        #rising is true if the sequence is increasing
        position = 1
        dampener = True
        rising = levels[0] < levels[-1]
        if seq_check(levels, position, rising, dampener):
            num_safe += 1
    return num_safe

if __name__ == '__main__':
    reports = load_reports(REPORTS_FILENAME)
    print("Number of safe reports:", safe_check(reports))
    