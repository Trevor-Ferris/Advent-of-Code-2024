"""
Advent of Code day 1 part 1
Written by Trevor Ferris
1/14/2025
"""

FILE_NAME = "Aoc1/input.txt"

def load_lists(file_name):
    values1 = []
    values2 = []
    inFile = open(file_name, 'r')
    for line in inFile:
        temp_value1 = int(line[:line.index(" ")].strip())
        temp_value2 = int(line[line.index(" "):].strip())
        values1.append(temp_value1)
        values2.append(temp_value2)
    return (values1, values2)

def distance_calc(dist_lists):
    dist_list1 = dist_lists[0]
    dist_list2 = dist_lists[1]
    dist_list1.sort()
    dist_list2.sort()
    tot_dist = 0
    for i in range(len(dist_list1)):
        tot_dist += (abs(dist_list1[i]-dist_list2[i]))
    return tot_dist

if __name__ == '__main__':
    dist_lists = load_lists(FILE_NAME)
    print("Distance between lists:", distance_calc(dist_lists))
