from cell import Cell
import time
import random


class Maze:

    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win,
                 seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.checked_cells = 0
        self.matrix_size = self.num_cols * self.num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        self._cells = self._create_cells()
        self._adj_dict = self.adj_dict()
        self._path_stack = [(0, 0)]
        self.run()

    def adj_dict(self):
        adj_dict = {}
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                temp_adj_cells = []
                for di, dj in directions:
                    new_i, new_j = i + di, j + dj
                    if 0 <= new_i < self.num_rows and 0 <= new_j < self.num_cols:
                        temp_adj_cells.append((new_i, new_j))
                adj_dict[(i, j)] = temp_adj_cells
        return adj_dict

    def _create_cells(self):
        cell_map = []
        for i in range(self.num_rows):
            row_list = []
            for j in range(self.num_cols):
                row_list.append(self._draw_cell(i, j))
            cell_map.append(row_list)
        return cell_map

    def _break_entrance_and_exit(self):
        self._cells[0][0].switch_left()
        self._cells[0][0].draw()
        self._cells[-1][-1].switch_right()
        self._cells[-1][-1].draw()

    def _break_walls_r(self, i, j):
        # Mark Current Cell as visited
        if not self._cells[i][j].visited:
            self._cells[i][j].visited = True
            self.checked_cells += 1
        # Create a loop
        while True:
            unvisited_places = []
            # create empty list to hold i,j values you need to visit
            # check for adjacency
            # impl adjacency dict
            adjacent_cells = self._adj_dict[(i, j)]
            for cell in adjacent_cells:
                if not self._cells[cell[0]][cell[1]].visited:
                    unvisited_places.append(cell)
            if self.checked_cells == self.matrix_size:
                self._cells[i][j].draw()
                return
            if unvisited_places:
                self._path_stack.append((i, j))
            else:
                prev = self._path_stack.pop()
                return self._break_walls_r(prev[0], prev[1])

            choice = unvisited_places.pop(random.randrange(len(unvisited_places)))

            # Need to knock down wall between two cells
            # Top
            if choice[0] == i + 1:
                self._cells[i][j].switch_right()
                self._cells[i][j].draw()
                self._cells[i + 1][j].switch_left()
                self._cells[i + 1][j].draw()
            # Bot
            if choice[0] == i - 1:
                self._cells[i][j].switch_left()
                self._cells[i][j].draw()
                self._cells[i - 1][j].switch_right()
                self._cells[i - 1][j].draw()
            # Right
            if choice[1] == j + 1:
                self._cells[i][j].switch_bot()
                self._cells[i][j].draw()
                self._cells[i][j + 1].switch_top()
                self._cells[i][j + 1].draw()
            # Left
            if choice[1] == j - 1:
                self._cells[i][j].switch_top()
                self._cells[i][j].draw()
                self._cells[i][j - 1].switch_bot()
                self._cells[i][j - 1].draw()

            self._previous_cell = ( i, j)
            return self._break_walls_r(choice[0], choice[1])

    def _draw_cell(self, i, j):
        cell = Cell(self.x1 + i * self.cell_size_x,
                    self.x1 + (i + 1) * self.cell_size_x,
                    self.y1 + j * self.cell_size_y,
                    self.y1 + (j + 1) * self.cell_size_y,
                    self.win)
        cell.draw()
        return cell

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def run(self):
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
