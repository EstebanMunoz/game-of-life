from dataclasses import astuple, dataclass

from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button, Header, Static


@dataclass
class GridLimits:
    """Class for keeping track of the grid screen limits."""

    top: int
    right: int
    bottom: int
    left: int

    def __iter__(self):
        return iter(astuple(self))


class GridInformation(Static):
    """Displays information about the grid"""

    limits = reactive(GridLimits(0, 0, 0, 0))

    def watch_limits(self) -> None:
        self.update(self.grid_information)

    @property
    def grid_information(self) -> str:
        top, right, bottom, left = self.limits
        info = f"Rows: {bottom}, {top} Cols: {left}, {right}"
        return info


class GridDisplay(Static):
    """A widget that shows the visible grid"""

    class SizeChanged(Message):
        """Custom Message that carries the new grid limits"""

        def __init__(self, limits) -> None:
            super().__init__()
            self.limits = limits

    limits = GridLimits(0, 0, 0, 0)
    dead_cell = "·"
    alive_cell = "■"  # Not used yet
    cells = ((0, 0), (1, 0), (0, 1), (-1, 1), (-1, 2), (-1, 3))

    def draw_cells(self) -> str:
        width, height = self.size
        cells = f"{self.dead_cell} " * ((width + 1) // 2) * height
        in_screen = []
        for cell in self.cells:
            if self.is_cell_in_screen(*cell):
                in_screen.append(cell)

        for cell in in_screen:
            coord = self.get_screen_coordinates(*cell)
            cells = f"{cells[:coord]}{self.alive_cell}{cells[coord+1:]}"

        return cells

    def is_cell_in_screen(self, row: int, col: int) -> bool:
        row_condition = self.limits.bottom <= row <= self.limits.top
        col_condition = self.limits.left <= col <= self.limits.right
        return row_condition and col_condition

    def get_screen_coordinates(self, row: int, col: int) -> int:
        if not self.is_cell_in_screen(row, col):
            raise ValueError("Cell is not in screen")

        screen_row = self.limits.top - row
        screen_col = (col - self.limits.left) * 2
        print(f"Width: {self.size.width} Height: {self.size.height}")
        print(f"Screen row: {screen_row} Screen col: {screen_col}")
        return (self.size.width + 1) // 2 * 2 * screen_row + screen_col

    def set_limits(self, width: int, height: int) -> None:
        left = -((width - 1) // 2) // 2
        right = ((width - 1) // 2) // 2
        top = (height - 1) // 2
        bottom = -(height - 1) // 2
        self.limits = GridLimits(top, right, bottom, left)

    def on_resize(self) -> None:
        width, height = self.size
        self.set_limits(width, height)
        self.post_message(self.SizeChanged(self.limits))
        self.update(self.draw_cells())


class GameOfLifeApp(App):
    TITLE = "Game of Life"
    SUB_TITLE = "By John Conway"
    CSS_PATH = "textual_app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(Center(GridInformation()), GridDisplay())
        yield Horizontal(
            Button("Next"), Button("Play"), Button("Stop"), Button("Reset")
        )

    def on_grid_display_size_changed(self, event: GridDisplay.SizeChanged) -> None:
        limits = event.limits
        self.query_one(GridInformation).limits = limits
