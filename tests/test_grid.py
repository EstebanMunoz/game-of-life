import pytest
import random

from src.game_of_life.grid import Grid


NUM_ROWS = 3
NUM_COLS = 3
NUM_RAND_TESTS = 20


@pytest.fixture
def grid() -> Grid:
    return Grid()


class TestGrid:
    def random_cell(self) -> tuple[int, int]:
        row = random.randint(-NUM_ROWS, NUM_ROWS)
        col = random.randint(-NUM_COLS, NUM_COLS)
        return row, col

    def test_init(self, grid: Grid) -> None:
        assert len(grid) == 0

        grid.set_cell(0, 0, 1)
        assert len(grid) == 1

        grid.set_cell(0, 0, 0)
        assert len(grid) == 0

    def test_get_cell(self, grid: Grid) -> None:
        for _ in range(NUM_RAND_TESTS):
            row, col = self.random_cell()
            assert grid[row, col] is not None
            assert grid[row, col] in [0, 1]

    def test_set_cell(self, grid: Grid) -> None:
        for _ in range(NUM_RAND_TESTS):
            row, col = self.random_cell()
            grid.set_cell(row, col, 1)
            assert grid[row, col] == 1

            grid.set_cell(row, col, 0)
            assert grid[row, col] == 0

            with pytest.raises(ValueError):
                grid.set_cell(row, col, 2)

            with pytest.raises(TypeError):
                grid.set_cell(row, col, "1")

    def test_alive_cells(self, grid: Grid) -> None:
        assert grid.alive_cells == ()

        grid.set_cell(0, 0, 1)
        assert grid.alive_cells == ((0, 0),)

        grid.set_cell(0, 1, 1)
        assert grid.alive_cells == ((0, 0), (0, 1))

        grid.set_cell(0, 0, 0)
        assert grid.alive_cells == ((0, 1),)
