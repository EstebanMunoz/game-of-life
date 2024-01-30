import curses

from grid import Grid
from driver import Driver


class Display:
    def __init__(
        self,
        grid: Grid | None = None,
        grid_style: str = "simple",
        padding: dict[str, int] | None = None,
    ) -> None:
        if grid is None:
            self.grid = Grid()
        else:
            self.grid = grid

        if padding is None:
            self.padding = {"top": 1, "bottom": 1, "left": 1, "right": 1}
        else:
            self.padding = padding

        self.grid_style = grid_style
        self.screen_rows, self.screen_cols = self.screen_limits(curses.initscr())
        self.left_limit = (
            -(
                (self.screen_cols + 1 - (self.padding["left"] + self.padding["right"]))
                // 2
                - 1
            )
            // 2
        )
        self.right_limit = (
            (self.screen_cols + 1 - (self.padding["left"] + self.padding["right"])) // 2
            - 1
        ) // 2
        self.top_limit = (
            -(self.screen_rows - (self.padding["top"] + self.padding["bottom"]) - 1)
            // 2
        )
        self.bottom_limit = (
            self.screen_rows - (self.padding["top"] + self.padding["bottom"]) - 1
        ) // 2

    def screen_limits(self, stdscr: curses.window) -> tuple[int, int]:
        max_y, max_x = stdscr.getmaxyx()
        return max_y, max_x

    def is_cell_in_screen(self, row: int, col: int) -> bool:
        row_condition = self.top_limit <= row <= self.bottom_limit
        col_condition = self.left_limit <= col <= self.right_limit
        return row_condition and col_condition

    def get_screen_coordinates(self, row: int, col: int) -> tuple[int, int]:
        if not self.is_cell_in_screen(row, col):
            raise ValueError("Cell is not in screen")
        screen_row = self.padding["top"] + row - self.top_limit
        screen_col = self.padding["left"] + (col - self.left_limit) * 2
        return screen_row, screen_col

    def print_cell(self, row: int, col: int, stdscr: curses.window) -> str:
        if self.is_cell_in_screen(row, col):
            screen_row, screen_col = self.get_screen_coordinates(row, col)
            stdscr.addstr(screen_row, screen_col, "■")

    def center_text(self, text: str, row: int, stdscr: curses.window) -> None:
        stdscr.addstr(row, (self.screen_cols - len(text)) // 2, text)

    def display(self, stdscr: curses.window) -> None:
        driver = Driver(self.grid)
        curses.curs_set(0)
        stdscr.nodelay(True)

        while True:
            key = stdscr.getch()
            if key == curses.KEY_LEFT:
                stdscr.clear()
                self.left_limit -= 1
                self.right_limit -= 1
            elif key == curses.KEY_RIGHT:
                stdscr.clear()
                self.left_limit += 1
                self.right_limit += 1
            elif key == curses.KEY_UP:
                stdscr.clear()
                self.top_limit -= 1
                self.bottom_limit -= 1
            elif key == curses.KEY_DOWN:
                stdscr.clear()
                self.top_limit += 1
                self.bottom_limit += 1
            elif key == ord(" "):
                driver.next_generation()
            elif key == ord("q"):
                curses.endwin()
                exit(0)

            game_status = f"Rows: {self.top_limit}, {self.bottom_limit}  Cols: {self.left_limit}, {self.right_limit}  Generation: {driver.generation}"
            instructions = (
                "q: exit  Spacebar: next generation  ←: left  →: right  ↑: up  ↓: down"
            )
            if len(game_status) < self.screen_cols:
                self.center_text(game_status, 0, stdscr)

            if len(instructions) < self.screen_cols:
                self.center_text(instructions, 1, stdscr)

            for row in range(
                self.padding["top"], self.screen_rows - self.padding["bottom"]
            ):
                for col in range(
                    self.padding["left"], self.screen_cols - self.padding["right"], 2
                ):
                    stdscr.addstr(row, col, "·")

            for row, col in self.grid.alive_cells:
                self.print_cell(row, col, stdscr)

            stdscr.refresh()
