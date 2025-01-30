#Advent of Code day 6 problem 2
#Made by Trevor Ferris
#1/17/2025

MAZE_FILENAME = "Documents\Python Practice\Aoc6\input.txt"

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

def count_X(maze):
    '''Counts the number of X's left by the travelling arrow'''
    num_X = 0
    for lines in maze:
        num_X += lines.count('X')
    return num_X

def move_arrow(maze, pos_x, pos_y, dir):
    '''Calculates the next position '''
    maze[pos_x][pos_y] = 'X'
    match dir:
        case '<':
            #check ahead if '#' change the direction if so
            if maze[pos_x][pos_y - 1] == '#':
                dir = change_dir(dir)
                return move_arrow(maze, pos_x, pos_y, dir)
            else:
                return (maze, pos_x, pos_y - 1, dir) 
        case 'v':
            if maze[pos_x + 1][pos_y] == '#':
                dir = change_dir(dir)
                return move_arrow(maze, pos_x, pos_y, dir)
            else:
                return (maze, pos_x + 1, pos_y, dir)
        case '>':
            if maze[pos_x][pos_y + 1] == '#':
                dir = change_dir(dir)
                return move_arrow(maze, pos_x, pos_y, dir)
            else:
                return (maze, pos_x, pos_y + 1, dir)
        case '^':
            if maze[pos_x - 1][pos_y] == '#':
                dir = change_dir(dir)
                return move_arrow(maze, pos_x, pos_y, dir)
            else:               
                return (maze, pos_x - 1, pos_y, dir)
            
def calc_path(maze, pos_x, pos_y, dir):
    '''moves the arrow around until it runs off the map'''
    while pos_x in range(len(maze)) and pos_y in range(len(maze[pos_x])):
        maze, pos_x, pos_y, dir = move_arrow(maze, pos_x, pos_y, dir)
    return maze

def checkMaze(maze):
    dirs = ['<', '^', '>', 'v']
    dir = ''
    pos_x, pos_y = 0, 0
    for line in maze:
        print(str(''.join(line)))
    for x in range(len(maze)):
        if any(value in dirs for value in maze[x]):
            for y in range(len(dirs)):
                if dirs[y] in maze[x]:
                    dir = dirs[y]
                    pos_x = x
                    pos_y = maze[x].index(dir)
    print("dir:", dir)
    print("posx:",pos_x)
    print("posy:",pos_y)
    maze = calc_path(maze, pos_x, pos_y, dir)
    for line in maze:
        print(str(''.join(line)))
    return count_X(maze)
       
if __name__ == ("__main__"):
    maze = load_maze(MAZE_FILENAME)
    print (checkMaze(maze))

