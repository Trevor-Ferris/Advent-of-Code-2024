"""
Advent of Code day 3 problem 1
Written by Trevor Ferris
1/15/2025
"""

REPORTS_FILENAME = "Aoc3/input.txt"

def load_reports(file_name):
    inFile = open(file_name, 'r')
    return inFile.read()

def find_muls(reports):
    muls = []
    mul_start = 0
    while mul_start != -1:
        mul_start = reports.find("mul(")
        reports = reports[mul_start:]
        temp_muls, mult1, mult2 = 0, 0, 0
        if reports.find(")") < 12:
            temp_muls = reports[4:reports.find(")")]           
            if temp_muls.find(",") != -1:
                mults = temp_muls.split(',')
                if len(mults[0]) <= 3 and mults[0].isdigit():
                    mult1 = int(mults[0])
                if len(mults[1]) <= 3 and mults[1].isdigit():
                    mult2 = int(mults[1])
                if mult1 > 0 and mult2 > 0:
                    muls.append((mult1, mult2))
            reports = reports[reports.find(")"):]
        else:
            reports = reports[1:]
    return muls

def multiply_muls(muls):
    total_val = 0
    for pairs in muls:
        total_val += (pairs[0] * pairs [1])
    return total_val

if __name__ == ("__main__"):
    reports = load_reports(REPORTS_FILENAME)
    muls = find_muls(reports)
    print("Multiplication results:", multiply_muls(muls))
