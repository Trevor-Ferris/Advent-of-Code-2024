#Advent of Code day 5 problem 1
#Made by Trevor Ferris
#1/17/2025

MANUALS_FILENAME = "Documents\Python Practice\Aoc5\input.txt"

def load_manuals(file_name):
    inFile = open(file_name)
    rules = {}
    pages = []
    for line in inFile:
        if line == '\n':
            continue
        line = line.replace('\n','')    
        if line.count('|'):
            rule = (list(map(int,line.split('|'))))
            if rule[0] in rules:
                rules[rule[0]].append(rule[1])
            else:
                rules[rule[0]] = [rule[1]]
        else:
            pages.append(list(map(int, line.split(','))))
    return (rules, pages)

def check_rules(page, rules, pos):
    if pos == len(page)-1:
        return True
    if any(value in rules[page[pos]] for value in page[0:pos]):
        return False
    return check_rules(page, rules, pos + 1)

def check_reports(rules, pages):
    mid_value = 0
    pos = 0
    for page in pages:
        if check_rules(page, rules, pos):
            mid = int(len(page)/2)
            mid_value += page[int(len(page)/2)]
    return mid_value
            
if __name__ == ("__main__"):
    rules, pages = load_manuals(MANUALS_FILENAME)
    print(check_reports(rules, pages))

