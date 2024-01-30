class Grid:
    def __init__(self) -> None:
        self._grid = dict()

    def set_cell(self, row: int, col: int, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("value must be an int")
        if value not in [0, 1]:
            raise ValueError("value must be 0 or 1")

        if value == 0:
            self._grid.pop((row, col), None)
            return
        self._grid[row, col] = value

    @property
    def alive_cells(self) -> tuple[tuple[int, int]]:
        return tuple(self._grid.keys())

    def clear(self) -> None:
        self._grid.clear()

    def __getitem__(self, indexes: tuple[int, int]) -> int:
        return self._grid.get(indexes, 0)

    def __len__(self) -> int:
        return len(self._grid)
