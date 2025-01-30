#Advent of Code day 5 problem 2
#Made by Trevor Ferris
#1/17/2025

MANUALS_FILENAME = "Documents\Python Practice\Aoc5\input.txt"

def load_manuals(file_name):
    inFile = open(file_name,'r')
    rules, rev_rules = {},{}
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
    return (rules, rev_rules, pages)

def check_rules(page, rules, pos):
    if pos == len(page):
        return True
    if rules.get(page[pos]):
        if any(value in rules[page[pos]] for value in page[0:pos]):
            return False
    return check_rules(page, rules, pos + 1)

def fix_report(page, rules, pos):
    if pos == len(page):
        return page
    if page[pos] in rules:
        for i in range(len(page)):
            if page[i] in rules[page[pos]]:
                page[pos], page[i] = page[i], page[pos]
                return fix_report(page, rules, pos)
    return fix_report(page, rules, pos + 1)
                    
def check_reports(rules, pages):
    mid_value, pos = 0, 0
    for page in pages:
        if check_rules(page, rules, pos):
            mid_value += page[int(len(page)/2)]
            print(page)
    return mid_value

def check_inc_reps(rules, pages):
    mid_value, pos = 0, 0
    for page in pages:
        if not check_rules(page, rules, pos):
            page = fix_report(page, rules, pos)
            mid_value += page[int(len(page)/2)]
    return mid_value

if __name__ == ("__main__"):
    rules, rev_rules, pages = load_manuals(MANUALS_FILENAME)
    print(check_inc_reps(rules, pages))

