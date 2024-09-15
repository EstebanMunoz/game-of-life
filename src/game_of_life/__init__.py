from game_of_life.model.grid import Grid
from game_of_life.ui.display import GameOfLifeApp

# def main() -> None:
#     grid = Grid()
#     grid.set_cell(0, 0, 1)
#     grid.set_cell(1, 0, 1)
#     grid.set_cell(0, 1, 1)
#     grid.set_cell(-1, 1, 1)
#     grid.set_cell(-1, 2, 1)
#     grid.set_cell(-1, 3, 1)

#     app = GameOfLifeApp(grid)
#     app.run()


grid = Grid()
grid.set_cell(0, 0, 1)
grid.set_cell(1, 0, 1)
grid.set_cell(0, 1, 1)
grid.set_cell(-1, 1, 1)
grid.set_cell(-1, 2, 1)
grid.set_cell(-1, 3, 1)

app = GameOfLifeApp(grid)
app.run()
