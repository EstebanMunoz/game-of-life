import pytest

from game_of_life.driver import Driver
from game_of_life.grid import Grid

NUM_ROWS = 5
NUM_COLS = 5


@pytest.fixture
def grid() -> Grid:
    return Grid()


@pytest.fixture
def driver(grid: Grid) -> Driver:
    return Driver(grid)


class TestDriver:
    def test_candidates(self, driver: Driver) -> None:
        driver.grid.set_cell(0, 0, 1)
        driver.grid.set_cell(1, 0, 1)
        driver.grid.set_cell(2, 0, 1)
        driver.grid.set_cell(0, 1, 1)

        candidates = driver.candidates
        sorted_candidates = tuple(sorted(candidates.items()))

        assert sorted_candidates == (
            ((-1, -1), 1),
            ((-1, 0), 2),
            ((-1, 1), 2),
            ((-1, 2), 1),
            ((0, -1), 2),
            ((0, 0), 2),
            ((0, 1), 2),
            ((0, 2), 1),
            ((1, -1), 3),
            ((1, 0), 3),
            ((1, 1), 4),
            ((1, 2), 1),
            ((2, -1), 2),
            ((2, 0), 1),
            ((2, 1), 2),
            ((3, -1), 1),
            ((3, 0), 1),
            ((3, 1), 1),
        )

    def test_next_generation(self, driver: Driver) -> None:
        driver.grid.set_cell(0, 0, 1)
        driver.grid.set_cell(1, 0, 1)
        driver.grid.set_cell(2, 0, 1)
        driver.grid.set_cell(0, 1, 1)
        driver.next_generation()

        next_generation = tuple(sorted(driver.grid.alive_cells))

        assert next_generation == (
            (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
        )
