from cell import Cell
import time


class Maze:

    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win,):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = self._create_cells()

    def _create_cells(self):
        cell_map = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell_map.append(self._draw_cell(i, j))
        self._break_entrance_and_exit(cell_map)
        return cell_map

    def _break_entrance_and_exit(self, cell_map):
        cell_map[0].switch_left()
        cell_map[-1].switch_right()
        cell_map[0].draw()
        self._animate()
        cell_map[-1].draw()
        self._animate()

    def _draw_cell(self, i, j):
        cell = Cell(self.x1 + i * self.cell_size_x,
                    self.x1 + (i + 1) * self.cell_size_x,
                    self.y1 + j * self.cell_size_y,
                    self.y1 + (j + 1) * self.cell_size_y,
                    self.win)
        cell.draw()
        self._animate()
        return cell

    def _animate(self):
        self.win.redraw()
        # time.sleep(0.05)
