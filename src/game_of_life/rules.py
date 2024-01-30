def game_rules(cell: int, alive_neighbors: int) -> int:
    alive_criterion = alive_neighbors == 3 or (alive_neighbors == 2 and cell == 1)
    return int(alive_criterion)
