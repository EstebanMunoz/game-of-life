import curses

from grid import Grid
from display import Display


grid = Grid()

grid.set_cell(0, 0, 1)
grid.set_cell(1, 0, 1)
grid.set_cell(0, 1, 1)
grid.set_cell(-1, 1, 1)
grid.set_cell(-1, 2, 1)
grid.set_cell(-1, 3, 1)


if __name__ == "__main__":
    padding = {"top": 2, "bottom": 2, "left": 2, "right": 2}
    display = Display(grid, padding=padding)
    try:
        curses.wrapper(display.display)
    except KeyboardInterrupt:
        exit(0)
