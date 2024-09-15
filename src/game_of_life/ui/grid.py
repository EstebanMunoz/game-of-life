from collections import namedtuple

from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from game_of_life.controller.driver import Driver
from game_of_life.model.grid import Grid

GridLimits = namedtuple("GridLimits", ["top", "right", "bottom", "left"])


class GridInformation(Static):
    """Displays information about the grid"""

    limits = reactive(GridLimits(0, 0, 0, 0))
    generation = reactive(1)

    def watch_limits(self) -> None:
        self.update(self.grid_information)

    def watch_generation(self):
        self.update(self.grid_information)

    @property
    def grid_information(self) -> str:
        top, right, bottom, left = self.limits
        info = f"Rows: {bottom}, {top} Cols: {left}, {right}"
        return f"{info}\nGeneration: {self.generation}"


class GridDisplay(Static):
    """A widget that shows the visible grid"""

    class SizeChanged(Message):
        """Custom Message that carries the new grid limits"""

        def __init__(self, limits: GridLimits) -> None:
            super().__init__()
            self.limits = limits

    limits = reactive(GridLimits(0, 0, 0, 0))

    def __init__(self, grid: Grid) -> None:
        super().__init__()
        self.driver = Driver(grid)
        self.dead_cell = "·"
        self.alive_cell = "■"

    def draw_cells(self) -> str:
        width, height = self.size
        cells = f"{self.dead_cell} " * ((width + 1) // 2) * height
        cells_in_screen = filter(self.is_cell_in_screen, self.driver.current_generation)

        for cell in cells_in_screen:
            coord = self.get_screen_coordinates(cell)
            cells = f"{cells[:coord]}{self.alive_cell}{cells[coord+1:]}"

        return cells

    def is_cell_in_screen(self, cell: tuple[int, int]) -> bool:
        row, col = cell
        row_condition = self.limits.bottom <= row <= self.limits.top
        col_condition = self.limits.left <= col <= self.limits.right
        return row_condition and col_condition

    def get_screen_coordinates(self, cell: tuple[int, int]) -> int:
        if not self.is_cell_in_screen(cell):
            raise ValueError("Cell is not in screen")

        row, col = cell
        screen_row = self.limits.top - row
        screen_col = (col - self.limits.left) * 2
        return ((self.size.width + 1) // 2) * 2 * screen_row + screen_col

    def set_limits(self, width: int, height: int) -> None:
        left = -((width - 1) // 2) // 2
        right = ((width - 1) // 2) // 2
        top = (height - 1) // 2
        bottom = -(height - 1) // 2
        self.limits = GridLimits(top, right, bottom, left)

    def on_resize(self) -> None:
        width, height = self.size
        self.set_limits(width, height)

    def watch_limits(self) -> None:
        self.post_message(self.SizeChanged(self.limits))
        self.update(self.draw_cells())
