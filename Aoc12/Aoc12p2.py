"""
Advent of code day 12 problem 1
Written by Trevor Ferris
1/25/2025
"""

from typing import Iterator

PLOTS_FILENAME = "input.txt"
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class plot(object):
    def __init__(self, letter:str):
        self.letter = letter
        self.walls = []
        self.connected = []
    
    def check_connected(self):
        return self.connected
    
    def update_connected(self, pos):
        self.connected.append(pos)

    def check_walls(self):
        return self.walls
    
    def update_walls(self, dir):
        self.walls.append(dir)
    
    def check_letter(self):
        return self.letter

def load_plots(file_name) -> list[list[plot]]:
    plots = []
    with open(file_name, "r") as plot_file:
        for row in plot_file:
            row = row.rstrip('\n')
            plot_row = []
            for col in row:
                plot_row.append(plot(col))
            plots.append(plot_row)
    return plots

def build_adj(plots, x, y):
    for dir in DIRS:
        new_x, new_y = x + dir[0], y + dir[1]
        if 0 <= new_x < len(plots) and 0 <= new_y < len(plots[0]):   
            if plots[new_x][new_y].check_letter() == plots[x][y].check_letter():
                plots[x][y].update_connected((new_x, new_y))
            else:
                plots[x][y].update_walls((dir))
        else:
                plots[x][y].update_walls((dir))

def check_walls(plots, x, y, dir) -> tuple[int]:
    num_adj = 0
    for adj_plot in plots[x][y].check_connected():
        if dir in plots[adj_plot[0]][adj_plot[1]].check_walls():
            num_adj += 1
    return (1 - num_adj, 0)
    
def check_adj(plots: list, x: int, y: int, checked: list) -> Iterator[tuple]:
    yield (0, 1)
    checked.append((x, y))
    build_adj(plots, x, y)
    for wall in plots[x][y].check_walls():
        yield check_walls(plots, x, y, wall)    
    for adj_plot in plots[x][y].check_connected():
        if adj_plot not in checked:
            yield from check_adj(plots, adj_plot[0], adj_plot[1], checked)
                
def check_plots(plots: list) -> int:
    """Run through a each plot start and then calculate cost based on results"""
    total = 0
    checked = []
    for x in range(len(plots)):
        for y in range(len(plots[x])):
            peri, area = 0, 0
            if (x, y) not in checked:
                peri_area = check_adj(plots, x, y, checked)
                for val in peri_area:
                    peri += val[0]
                    area += val[1]
                print(area, peri, plots[x][y].check_letter())
                total += (peri * area)
    return total

def main():
    plots = load_plots(PLOTS_FILENAME)
    print(check_plots(plots))
    print("done")

if __name__ == ("__main__"):
    main()