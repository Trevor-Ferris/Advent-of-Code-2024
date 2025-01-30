#Advent of Code day 9 problem 2
#Made by Trevor Ferris
#1/20/2025

DISKMAP_FILENAME = "input.txt"

class mem_block(object):
    def __init__(self, val, n_vals, n_spaces):
        self.val = val
        self.n_vals = n_vals
        self.n_spaces = n_spaces
        self.blocks = None
    
    def get_val(self):
        return self.val
    
    def get_n_vals(self):
        return self.n_vals
    
    def get_n_spaces(self):
        return self.n_spaces
    
    def get_filled(self):
        return self.blocks
    
    def get_all(self):
        return (self.val, self.n_vals, self.n_spaces)
    
    def update_n_spaces(self, n):
        self.n_spaces = n
    
    def change_n_spaces(self, n):
        self.n_spaces += n
    
    def remove_fill(self):
        self.blocks = None

    def fill_space(self, block):
        if self.blocks:
            print(self.blocks.get_val())
            self.blocks.fill_space(block)
        else:
            block.update_n_spaces(0)
            self.blocks = block

    def copy(self):
        return mem_block(self.val, self.n_vals, self.n_spaces)
    
def load_map(file_name):
    inFile = open(file_name, 'r')
    for line in inFile:
        line = line.replace('\n', '')
        disk_map = line
    return disk_map

def copy_disk(disk):
    new_disk = []
    for block in disk:
        new_disk.append(block.copy())
    return new_disk        

def gen_disk(disk_map):
    disk = []
    for id in range(0, len(disk_map), 2):
        if id + 1 in range(len(disk_map)):
            n_spaces = int(disk_map[id + 1])
        else:
            n_spaces = 0
        n_vals = int(disk_map[id])
        disk.append(mem_block(int(id / 2), n_vals, n_spaces))
    return disk

def print_disk(disk):
    for block in disk:
        print(block.get_all())

def disk_str_help(block):
    disk_list = ''
    for i in range(block.get_n_vals()):
        disk_list += str(block.get_val())
    if block.get_filled():
        disk_list += disk_str_help(block.get_filled())
    for i in range(block.get_n_spaces()):
        disk_list += ('.')
    return disk_list

def gen_disk_str(disk):
    disk_list = ''
    for block in disk:
        disk_list += disk_str_help(block)
    return disk_list

def check_block(disk, index1, block1, start_index):
    for index2, block2 in enumerate(copy_disk(disk)[start_index:index1]):
        if block2.get_n_spaces() >= block1.get_n_vals():
            new_block = disk.pop(index1)
            if new_block.get_filled():
                disk.insert(index1, new_block.get_filled())
                disk[index1].change_n_spaces(new_block.get_n_spaces())
                disk[index1 - 1].change_n_spaces(new_block.get_n_vals())
                new_block.remove_fill()
            else:
                disk[index1 - 1].change_n_spaces(new_block.get_n_vals() + new_block.get_n_spaces())
            disk[index2].change_n_spaces(-new_block.get_n_vals())
            disk[index2].fill_space(new_block)       
            while disk[start_index].get_n_spaces() == 0:
                start_index += 1
                if start_index == index1:
                    break
            break
    return (disk, start_index)

def defrag_disk(disk):
    start_index = 0
    for index1, block1 in reversed(list(enumerate(copy_disk(disk)))):
        disk, start_index = check_block(disk, index1, block1, start_index)
        if start_index == index1:
            break

    return disk     


''' """Python"""
def gen_disk_list(disk):
    pos = disk[0]
    disk_list = []
    while pos:
        for i in range(pos.get_n_vals()):
            disk_list.append(pos.get_val())
        for i in range(pos.get_n_spaces()):
            disk_list.append('.')
        pos = pos.get_nxt()
    return disk_list

def print_disk(disk):
    pos = disk[0]
    while pos:
        print(pos.get_all())
        pos = pos.get_nxt()

def block_defrag(disk):
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
    return disk'''           

'''memorial comment
def gen_block_dict(disk_map): 
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

def check_sum(disk_str):
    sum = 0
    disk_list = list(disk_str)
    for index, value in enumerate(disk_list):
        if value == '.':
            continue
        sum += index * int(value)
    return sum

if __name__ == ('__main__'):
    disk_map = load_map(DISKMAP_FILENAME)
    print("diskmap loaded")
    disk = gen_disk(disk_map)
    def_disk = defrag_disk(copy_disk(disk))
    for block in def_disk:
        print(block.get_val())
    print(gen_disk_str(def_disk))
    print(check_sum(gen_disk_str(def_disk)))

    

