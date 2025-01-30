"""
Advent of Code day 9 part 1
Written by Trevor Ferris
1/20/2025
"""

DISKMAP_FILENAME = "Aoc9/input.txt"

def load_map(file_name):
    inFile = open(file_name, 'r')
    for line in inFile:
        line = line.replace('\n', '')
        disk_map = line
    return disk_map

def gen_blocks(disk_map):
    blocks = []
    count = 0
    id_num = 0
    while True:
        for i in range(int(disk_map[count])):
            blocks.append(id_num)
        count += 1
        id_num += 1
        if count == len(disk_map):
            break
        for i in range(int(disk_map[count])):
            blocks.append('.')
        count += 1
        if count == len(disk_map):
            break        
    return blocks

def defrag(blocks):
    while '.' in blocks:
        dot_loc = blocks.index('.')
        blocks[dot_loc], blocks[-1] = blocks[-1], blocks[dot_loc]
        while blocks[-1] == '.':
            blocks.pop(-1)        
    return blocks

def check_sum(blocks):
    sum = 0
    for index, value in enumerate(blocks):
        sum += index * value
    return sum

if __name__ == ('__main__'):
    disk_map = load_map(DISKMAP_FILENAME)
    print("Diskmap loaded")
    blocks = gen_blocks(disk_map)
    print("Disk built")
    print("Fragmenting...")
    def_blocks = defrag(blocks.copy())
    print("Check sum:", check_sum(def_blocks))
