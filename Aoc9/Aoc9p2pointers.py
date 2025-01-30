"""
Advent of Code day 9 part 2
Written by Trevor Ferris
1/20/2025
Notes: Jank implementation using pointers from a list
"""

DISKMAP_FILENAME = "Aoc9/input.txt"

class mem_block(object):
    def __init__(self, val, n_vals, n_spaces):
        self.val = val
        self.n_vals = n_vals
        self.n_spaces = n_spaces
        self.prev = None
        self.nxt = None
    
    def get_val(self):
        return self.val
    
    def get_n_vals(self):
        return self.n_vals
    
    def get_n_spaces(self):
        return self.n_spaces
    
    def get_prev(self):
        return self.prev
    
    def get_nxt(self):
        return self.nxt
    
    def get_all(self):
        return (self.val, self.n_vals, self.n_spaces, self.prev, self.nxt)
    
    def update_n_spaces(self, n):
        self.n_spaces = n
    
    def update_prev(self, n):
        self.prev = n
    
    def update_nxt(self, n):
        self.nxt = n

def load_map(file_name):
    inFile = open(file_name, 'r')
    for line in inFile:
        line = line.replace('\n', '')
        disk_map = line
    return disk_map

def gen_disk(disk_map):
    disk = []
    for id in range(0, len(disk_map), 2):
        if id + 1 in range(len(disk_map)):
            n_spaces = int(disk_map[id + 1])
        else:
            n_spaces = 0
        n_vals = int(disk_map[id])
        disk.append(mem_block(int(id / 2), n_vals, n_spaces))
        if id != 0:
            disk[int(id / 2)].update_prev(disk[int(id / 2 ) - 1])
            disk[int(id / 2 ) - 1].update_nxt(disk[int(id / 2)])
    return disk

def gen_disk_list(disk: list[mem_block]):
    pos = disk[0]
    disk_list = []
    while pos:
        for i in range(pos.get_n_vals()):
            disk_list.append(pos.get_val())
        for i in range(pos.get_n_spaces()):
            disk_list.append('.')
        pos = pos.get_nxt()
    return disk_list

def print_disk(disk: list[mem_block]):
    pos = disk[0]
    while pos:
        print(pos.get_all())
        pos = pos.get_nxt()

def block_defrag(disk: list[mem_block]):
    back_pos = disk[len(disk) - 1]
    start_pos = disk[0]
    while start_pos != back_pos:
        pos = start_pos
        next_pos = back_pos.get_prev()
        while pos.get_val() != back_pos.get_val():
            #print(pos.get_val(), back_pos.get_val())
            if pos.get_n_spaces() >= back_pos.get_n_vals():                
                #remove back pos from the disk, update the previous values pointer and spaces, update the next blocks pointer
                back_pos.get_prev().update_nxt(back_pos.get_nxt())
                if back_pos.get_nxt():
                    back_pos.get_nxt().update_prev(back_pos.get_prev())
                back_pos.get_prev().update_n_spaces(back_pos.get_prev().get_n_spaces() + back_pos.get_n_vals() + back_pos.get_n_spaces())
                #insert block into space update pointers and spaces
                back_pos.update_prev(pos)
                back_pos.update_nxt(pos.get_nxt())
                pos.get_nxt().update_prev(back_pos)
                pos.update_nxt(back_pos)
                back_pos.update_n_spaces(pos.get_n_spaces() - back_pos.get_n_vals())
                pos.update_n_spaces(0)
                #set the search start pos to the moved block, or the next block if this block has no space
                while start_pos.get_n_spaces() == 0:
                    start_pos = start_pos.get_nxt()
                    if start_pos == next_pos:
                        break
            pos = pos.get_nxt()    
        back_pos = next_pos
    return disk         

def check_sum(disk_list):
    sum = 0
    for index, value in enumerate(disk_list):
        if value == '.':
            continue
        sum += index * value
    return sum

if __name__ == ('__main__'):
    disk_map = load_map(DISKMAP_FILENAME)
    print("diskmap loaded")
    disk = gen_disk(disk_map)
    print("disk built")
    print("defragmenting...")
    disk = block_defrag(disk)
    print("Check sum:", check_sum(gen_disk_list(disk)))

    

