#Advent of Code day 9 problem 2
#Made by Trevor Ferris
#1/20/2025

DISKMAP_FILENAME = "inputtest.txt"

class mem_block(object):
    def __init__(self, val, n_vals, n_spaces, prev, nxt):
        self.val = val
        self.n_vals = n_vals
        self.n_spaces = n_spaces
        self.prev = prev
        self.nxt = nxt
    
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
        self.n_spaces += n
    
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
        if id + 2 in range(len(disk_map)):
            point_to = int((id + 2) / 2)
        else:
            point_to = 0
        if id + 1 in range(len(disk_map)):
            n_spaces = int(disk_map[id + 1])
        else:
            n_spaces = 0
        if id > 0:
            point_from = int(id / 2) - 1
        else:
            point_from = 0
        n_vals = int(disk_map[id])
        disk.append(mem_block(int(id / 2), n_vals, n_spaces, point_from, point_to))    
    return disk

def gen_disk_list(disk):
    pos = 0
    disk_list = []
    while True:
        for i in range(disk[pos].get_n_vals()):
            disk_list.append(pos)
        for i in range(disk[pos].get_n_spaces()):
            disk_list.append('.')
        pos = disk[pos].get_nxt()
        if pos == 0:
            break
    return disk_list

def block_defrag(disk):
    back_pos = len(disk) - 1
    while True:
        pos = 0
        while disk[pos].get_val() != disk[back_pos].get_val():
            print(back_pos, pos)
            if disk[pos].get_n_spaces() >= disk[back_pos].get_n_vals():
                #remove back pos from the disk, update the previous values pointer and spaces, update the next blocks pointer
                disk[disk[back_pos].get_prev()].update_n_spaces(disk[back_pos].get_n_vals())
            pos = disk[pos].get_nxt()
        
        back_pos = disk[back_pos].get_prev()
        if back_pos == 0:
            break

    pass            

'''def gen_block_dict(disk_map): memorial comment
    block_dict = {}
    for i in range(0, len(disk_map), 2):
        if i + 2 in range(len(disk_map)):
            point_to = int((i + 2) / 2)
        else:
            point_to = 0
        if i > 0:
            point_from = i / 2
        else:
            point_from = 0
        block_dict[int(i / 2)] = [int(disk_map[i]), 0, point_to, point_from]
    for i in range(1, len(disk_map), 2):
        block_dict[int((i - 1) / 2)][1] = int(disk_map[i])    
    return block_dict

def gen_block_list(block_dict):
    block_list = []
    pos = 0
    while True:
        for i in range(block_dict[pos][0]):
            block_list.append(pos)
        for i in range(block_dict[pos][1]):
            block_list.append('.')
        pos = block_dict[pos][2]
        if pos == 0:
            break
    return block_list

def defrag(block_dict):
    for i in reversed(range(len(block_dict))):
        pos = 0
        start_pos = i
        while pos != start_pos:
            print("test")
            if block_dict[pos][1] >= block_dict[start_pos][0]:
                #make the block before the moving block point to the pointer of the moving block
                block_dict[block_dict[start_pos][3]][2] = block_dict[start_pos][2]
                #make the block ahead point from the previous block
                block_dict[block_dict[start_pos][2]][3] = block_dict[start_pos][2]
                #update block 
                block_dict[start_pos][3] = block_dict[pos]
                block_dict[block_dict[pos][2]][3] = block_dict[start_pos]
                #make the block point to the moving block and the new block point to the pointer of the current block
                block_dict[pos][2], block_dict[start_pos][2] = start_pos, block_dict[pos][2]             
                #make the block before the moving block get space from the total amount of the moving block
                block_dict[start_pos - 1][1] += block_dict[start_pos][0] + block_dict[start_pos][1]
                #update the space of the current block to 0 and the moving block to the difference between the empty space and the size
                block_dict[start_pos][1] = block_dict[pos][1] - block_dict[start_pos][0]
                block_dict[pos][1] = 0
                print(''.join(str(x) for x in gen_block_list(block_dict)))
                print(block_dict)
            
            pos = block_dict[pos][2]
    return block_dict'''

def check_sum(blocks):
    sum = 0
    for index, value in enumerate(blocks):
        sum += index * value
    return sum

if __name__ == ('__main__'):
    disk_map = load_map(DISKMAP_FILENAME)
    print("diskmap loaded")
    disk = gen_disk(disk_map)
    for item in disk:
        print(item.get_all())
    print("disk built")
    block_defrag(disk)
    print(''.join(str(x) for x in gen_disk_list(disk)))

