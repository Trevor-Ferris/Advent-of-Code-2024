#Advent of Code day 6 problem 2
#Made by Trevor Ferris
#1/17/2025

MAZE_FILENAME = "input.txt"

def load_maze(file_name):
    inFile = open(file_name, 'r')
    maze = []
    for line in inFile:
        line = line.replace('\n', '')
        a = [ch for ch in line]
        maze.append(a)
    return maze

def change_dir(dir):
    '''Turns the direction of the arrow given to the right'''
    dirs = ['<', 'v', '>', '^']
    new_dir = dirs[dirs.index(dir) - 1]
    return new_dir

def calc_next_pos(pos_x, pos_y, dir):
    '''returns the number direction of the arrow'''    
    match dir:
        case '<':
            pos_y -= 1
        case '>':
            pos_y += 1
        case 'v':
            pos_x += 1
        case '^':
            pos_x -=1
    return(pos_x, pos_y)

def maze_copy(maze):
    '''returns a deepcopy of maze'''
    new_maze = []
    for item in maze:
        new_maze.append(list(item))
    return new_maze
          
def calc_path(maze, pos_x, pos_y, dir):
    '''moves the arrow around until it runs off the map placing an recording a set of coordinates that have been pathed through'''
    marked = set({})
    while True:
        marked.add((pos_x, pos_y))
        next_x, next_y = calc_next_pos(pos_x, pos_y, dir)
        if next_x in range(len(maze)) and next_y in range(len(maze[pos_x])):
            if maze[next_x][next_y] == '#':
                dir = change_dir(dir)
            else:          
                pos_x, pos_y = next_x, next_y
        else:
            break
    return len(marked)

def check_loop(maze, pos_x, pos_y, dir):
    '''records for each direction which obstacles it has hit, if the pathing hits the same obstacle from the same direction then a loop has been made
        otherwise if the arrow goes out of bounds there is no loop'''
    bounced = {'<' : [], 'v' : [], '>' : [], '^' : []}
    while True:
        next_x, next_y = calc_next_pos(pos_x, pos_y, dir)
        if next_x in range(len(maze)) and next_y in range(len(maze[pos_x])):
            if maze[next_x][next_y] == '#':
                if (next_x, next_y) in bounced[dir]:
                    return True
                else:
                    bounced[dir].append((next_x, next_y))
                    dir = change_dir(dir)
            else:       
                pos_x, pos_y = next_x, next_y
        else:
            break
    return False

def calc_loops(maze, pos_x, pos_y, dir):
    '''Runs maze testing a maze at each position where a '#' is placed directly ahead of the current position
        records a set of coordinates where the '#' creates a loop'''
    start_x, start_y, start_dir = pos_x, pos_y, dir
    loops = set({})
    while True:
        next_x, next_y = calc_next_pos(pos_x, pos_y, dir)
        if next_x in range(len(maze)) and next_y in range(len(maze[pos_x])):
            if maze[next_x][next_y] == '#':
                dir = change_dir(dir)
            else:
                loop_maze = maze_copy(maze)
                loop_maze[next_x][next_y] = '#'
                if check_loop(loop_maze, start_x, start_y, start_dir):
                    loops.add((next_x, next_y))            
                pos_x, pos_y = next_x, next_y
        else:
            break
    return len(loops)

def maze_start(maze):
    dirs = ['<', 'v', '>', '^']
    dir = ''
    pos_x, pos_y = 0, 0
    for x in range(len(maze)):
        if any(value in dirs for value in maze[x]):
            for y in range(len(dirs)):
                if dirs[y] in maze[x]:
                    dir = dirs[y]
                    pos_x = x
                    pos_y = maze[x].index(dir)
    return (pos_x, pos_y, dir)
       
if __name__ == ("__main__"):
    maze = load_maze(MAZE_FILENAME)
    pos_x, pos_y, dir = maze_start(maze)
    print("Path Length:", calc_path(maze_copy(maze), pos_x, pos_y, dir))
    print("Checking number of loops...")
    print("Number of loops:", calc_loops(maze_copy(maze), pos_x, pos_y, dir))

