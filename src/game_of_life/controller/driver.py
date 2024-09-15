from collections import defaultdict

from game_of_life.model.grid import Grid
from game_of_life.model.rules import game_rules


class Driver:
    def __init__(self, grid: Grid | None = None) -> None:
        self.initial_grid = grid
        if grid is None:
            self.initial_grid = Grid()

        self.grid = self.initial_grid.copy()
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

    @property
    def current_generation(self) -> tuple[tuple[int, int]]:
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

    def reset_generations(self) -> None:
        self.grid = self.initial_grid.copy()
        self.generation = 1
