from collections import defaultdict

from game_of_life.rules import game_rules
from game_of_life.grid import Grid


class Driver:
    def __init__(self, grid: Grid | None = None) -> None:
        if grid is None:
            self.grid = Grid()
        else:
            self.grid = grid
        self.generation = 1

    @property
    def candidates(self) -> defaultdict:
        alive_cells = self.grid.alive_cells
        candidate_cells = defaultdict(int)
        for x, y in alive_cells:
            candidate_cells[x - 1, y - 1] += 1
            candidate_cells[x - 1, y] += 1
            candidate_cells[x - 1, y + 1] += 1
            candidate_cells[x, y - 1] += 1
            candidate_cells[x, y + 1] += 1
            candidate_cells[x + 1, y - 1] += 1
            candidate_cells[x + 1, y] += 1
            candidate_cells[x + 1, y + 1] += 1

        return candidate_cells

    def alive_neighbors(self, row: int, col: int) -> int:
        return self.candidates[row, col]

    @property
    def current_generation(self):
        return self.grid.alive_cells

    def next_generation(self) -> None:
        alive_cells = self.grid.alive_cells
        candidates = self.candidates
        self.grid.clear()
        for row, col in candidates:
            neighbors = candidates[row, col]
            current_state = int((row, col) in alive_cells)
            new_state = game_rules(current_state, neighbors)
            self.grid.set_cell(row, col, new_state)

        self.generation += 1
