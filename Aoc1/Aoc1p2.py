#Advent of Code day 1 problem 2
#Made by Trevor Ferris
#1/14/2025
FILE_NAME = "Documents\Python Practice\Aoc1\input.txt"
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
def similar_calc(dist_lists):
    dist_list1 = dist_lists[0]
    dist_list2 = dist_lists[1]
    sim_score = 0
    for i in range(len(dist_list1)):
        sim_score += dist_list1[i]*dist_list2.count(dist_list1[i])
    return sim_score

if __name__ == '__main__':
    dist_lists = load_lists(FILE_NAME)
    print(similar_calc(dist_lists))
