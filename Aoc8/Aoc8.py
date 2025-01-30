"""
Advent of Code day 8 part 2
Written by Trevor Ferris
1/20/2025
Notes: Part 1 is lost
"""

MAP_FILENAME = "Aoc8/input.txt"

def load_map(file_name):
    inFile = open(file_name, 'r')
    syg_map = []
    for line in inFile:
        line = line.replace('\n', '')
        a = [ch for ch in line]
        syg_map.append(a)
    return syg_map

def build_dict(syg_map):
    tower_dict = {}
    for index_1, row in enumerate(syg_map):
        for index_2, column in enumerate(row):
            if column != '.':
                if tower_dict.get(column):
                    tower_dict[column].append((index_1, index_2))
                else:
                    tower_dict[column] = [(index_1, index_2)]
    return tower_dict

def nodes_forward(pos, vect, max):
    antinodes = []
    while (pos[0] in range(max[0]) and pos[1] in range(max[1])):
        antinodes.append(pos)
        pos = tuple(map(lambda i, j: i - j, pos, vect))       
    return antinodes

def check_antinodes(tower_dict, syg_map):
    max_x, max_y = len(syg_map), len(syg_map[0])
    tot_anti = set({})
    for node in tower_dict:
        for index, coord in enumerate(tower_dict[node]):
            for coord2 in tower_dict[node][index+1:]:
                (x, y) = tuple(map(lambda i, j: i - j, coord, coord2))
                antinodes = nodes_forward(coord,(x, y), (max_x, max_y))
                antinodes.extend(nodes_forward(coord2,(-x, -y), (max_x, max_y)))
                for x in antinodes:
                    tot_anti.add(x)
    return len(tot_anti)

if __name__ == ('__main__'):
    syg_map = load_map(MAP_FILENAME)
    tower_dict = build_dict(syg_map)
    print("Number of antinodes:", check_antinodes(tower_dict, syg_map))
