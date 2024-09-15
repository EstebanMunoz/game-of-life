from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Button, Header

from game_of_life.model.grid import Grid
from game_of_life.ui.grid import GridDisplay, GridInformation


class GameOfLifeApp(App):
    TITLE = "Game of Life"
    SUB_TITLE = "By John Conway"
    CSS_PATH = "game_of_life.tcss"

    BINDINGS = [
        ("left", "move_grid('left')", "Moves the grid one unit left"),
        ("right", "move_grid('right')", "Moves the grid one unit right"),
        ("up", "move_grid('top')", "Moves the grid one unit up"),
        ("down", "move_grid('bottom')", "Moves the grid one unit down"),
    ]

    def __init__(self, grid: Grid) -> None:
        super().__init__()
        self.grid = grid

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Center():
                yield GridInformation()
            yield GridDisplay(self.grid)
        with Horizontal():
            yield Button(" Next", id="next")
            yield Button(" Play", id="play")
            yield Button(" Stop", id="stop")
            yield Button("󰜉 Reset", id="reset")

    def on_grid_display_size_changed(self, event: GridDisplay.SizeChanged) -> None:
        limits = event.limits
        self.query_one(GridInformation).limits = limits

    @on(Button.Pressed, "#next")
    def call_next_generation(self) -> None:
        grid_display = self.query_one(GridDisplay)
        grid_info = self.query_one(GridInformation)
        grid_display.driver.next_generation()
        grid_info.generation = grid_display.driver.generation
        grid_display.update(grid_display.draw_cells())

    @on(Button.Pressed, "#reset")
    def call_reset(self) -> None:
        grid_display = self.query_one(GridDisplay)
        grid_info = self.query_one(GridInformation)
        grid_display.driver.reset_generations()
        grid_info.generation = grid_display.driver.generation
        grid_display.update(grid_display.draw_cells())

    @on(Button.Pressed, "#play")
    def call_play(self) -> None:
        self.add_class("playing")
        self.query_one("#next").disabled = True
        self.query_one("#reset").disabled = True

    @on(Button.Pressed, "#stop")
    def call_stop(self) -> None:
        self.remove_class("playing")
        self.query_one("#next").disabled = False
        self.query_one("#reset").disabled = False

    def action_move_grid(self, direction: str) -> None:
        grid_display = self.query_one(GridDisplay)
        limits = grid_display.limits
        match direction:
            case "left":
                left = limits.left - 1
                right = limits.right - 1
                limits = limits._replace(left=left, right=right)
            case "right":
                left = limits.left + 1
                right = limits.right + 1
                limits = limits._replace(left=left, right=right)
            case "top":
                top = limits.top + 1
                bottom = limits.bottom + 1
                limits = limits._replace(top=top, bottom=bottom)
            case "bottom":
                top = limits.top - 1
                bottom = limits.bottom - 1
                limits = limits._replace(top=top, bottom=bottom)
        grid_display.limits = limits
