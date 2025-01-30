"""
Advent of code day 12 problem 1
Written by Trevor Ferris
1/25/2025
"""

from typing import Iterator

PLOTS_FILENAME = "input.txt"
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def load_plots(file_name):
    plot_starts = {}
    plots = []
    with open(file_name, "r") as plot_file:
        for x, row in enumerate(plot_file):
            row = row.rstrip('\n')
            plot_row = []
            for y, col in enumerate(row):
                if not plot_starts.get(col):
                    plot_starts[col] = (x, y)
                plot_row.append(col)
            plots.append(plot_row)
    return (plots, plot_starts)

def check_adj(plots: list, pos: tuple, checked: list) -> Iterator[tuple]:
    yield (0, 1)
    checked.append(pos)
    for dir in DIRS:
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if 0 <= new_pos[0] < len(plots) and 0 <= new_pos[1] < len(plots[0]):
            if plots[new_pos[0]][new_pos[1]] != plots[pos[0]][pos[1]]:
                yield (1, 0)
            elif not new_pos in checked:
                yield from check_adj(plots, new_pos, checked)
        else:
            yield (1, 0)


def check_plots(plots: list, plot_starts: dict) -> int:
    """Run through a each plot start and then calculate cost based on results"""
    total = 0
    checked = []
    for x in range(len(plots)):
        for y in range(len(plots[x])):
            peri, area = 0, 0
            if (x, y) not in checked:
                peri_area = check_adj(plots, (x, y), checked)
                for val in peri_area:
                    peri += val[0]
                    area += val[1]
                print(area, peri, plots[x][y])
                total += (peri * area)
    return total

def main():
    plots, plot_starts = load_plots(PLOTS_FILENAME)
    print(check_plots(plots, plot_starts))
    print("done")

if __name__ == ("__main__"):
    main()
                