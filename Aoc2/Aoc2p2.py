#Advent of Code day 2 problem 1
#Made by Trevor Ferris
#1/14/2025
REPORTS_FILENAME = "Documents\Python Practice\Aoc2\input.txt"
def load_reports(file_name):
    inFile = open(file_name, 'r')
    reports = []
    for line in inFile:
        reports.append(list(map(int, line.split())))
    return reports
def seq_check(levels, position, direction, dampener):

    if position == len(levels):
        if not dampener:
            print(levels)
        return True
     #if the change is more than 3 return false
    if (abs(levels[position-1]-levels[position])>3):
        if dampener:
            levels_check1 = levels.copy()
            levels_check2 = levels.copy()
            levels_check1.pop(position)
            levels_check2.pop(position-1)
            removed_here = seq_check(levels_check1,position,direction,False)
            removed_prev = seq_check(levels_check2,position,direction,False)
            if removed_here or removed_prev:
                print(levels)
            return removed_here or removed_prev
        else:
            return False
    #if the next level is in the same direction as before then recursively call either until it is not or until it is the last position
    elif (levels[position-1] < levels[position]) and direction:
        return seq_check(levels, (position+1), direction, dampener)
    elif (levels[position-1] > levels[position])  and not direction:
        return seq_check(levels, (position+1), direction, dampener)
    else:
        if dampener:
            levels_check1 = levels.copy()
            levels_check2 = levels.copy()
            levels_check1.pop(position)
            levels_check2.pop(position-1)
            removed_here = seq_check(levels_check1,position,direction,False)
            removed_prev = seq_check(levels_check2,position,direction,False)
            if removed_here or removed_prev:
                print(levels)
            return removed_here or removed_prev
        else:
            return False
def dampener(levels,pos,rising):
#dampener logic
#if the function is going in the wrong direction for one value check the previous value
    if ((levels[pos-1] < levels[pos])  and not rising) or ((levels[pos-1] > levels[pos]) and rising):
        return ((levels[pos-2] < levels[pos])  and not rising) or ((levels[pos-2] > levels[pos]) and rising)
#if the function is has a value that is too high check the next value against the previous value
    if (abs(levels[pos-1] - levels[pos])>3):
        return (abs(levels[pos-1] - levels[pos])>3)
#if a function has been given the wrong direction as a result of the second value being wrong change the direction
    if ((levels[0] < levels[i])  and not rising) or ((levels[0] > levels[i]) and rising)
def safe_check(reports):
    num_safe = 0
    for levels in reports:
        #direction is true if the sequence is increasing
        dampener = True
        rising = levels[0] < levels[1]
        prev_val = None
        for i in range(len(levels)):
            print (levels)
            if prev_val != None:
                if (abs(levels[prev_val] - levels[i])>3):
                    if dampener:
                        if ((levels[0] < levels[i])  and not rising) or ((levels[0] > levels[i]) and rising):
                            rising = not rising
                        dampener = False
                        if i == len(levels)-1:
                            num_safe +=1
                        continue
                    else:
                        break
                elif(levels[prev_val] < levels[i]) and rising:
                    prev_val = i
                    if i == len(levels)-1:
                        num_safe +=1
                    continue
                elif (levels[prev_val] > levels[i])  and not rising:
                    prev_val = i
                    if i == len(levels)-1:    
                        num_safe +=1
                    continue
                else:
                    if dampener:
                        dampener = False
                        print(levels)
                        if ((levels[0] < levels[i])  and not rising) or ((levels[0] > levels[i]) and rising):
                            rising = not rising
                        if i == len(levels)-1:
                            num_safe +=1
                        continue
                    break
            else:
                prev_val = i
                


    

    return num_safe



if __name__ == '__main__':

    reports = load_reports(REPORTS_FILENAME)
    print(reports)
    print(safe_check(reports))