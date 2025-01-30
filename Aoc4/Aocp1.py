#Advent of Code day 1 problem 1
#Made by Trevor Ferris
#1/17/2025

REPORTS_FILENAME = "Documents\Python Practice\Aoc4\input.txt"

def load_reports(file_name):
    inFile = open(file_name)
    reports = []
    for line in inFile:
        reports.append(line.read())
    return reports

if __name__ == ("__main__"):
    reports = load_reports(REPORTS_FILENAME)
    print (reports)
