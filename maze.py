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
        self._path_wall_stack = {}
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

    def _create_path_wall_stack(self):
        wall_dict = {}
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                wall_dict[(i, j)] = self._set_list_input(i, j)
        return wall_dict

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
                self._reset_cells_visited()
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
        self._path_stack = []
        self._path_wall_stack = self._create_path_wall_stack()

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        # Only add the wall info if we haven't visited
        self._path_wall_stack[(i, j)] = self._set_list_input(i, j)

        # Add the path to our stack
        self._path_stack.append((i, j))
        # Made it to the end end of our path
        if self._cells[i][j] == self._cells[-1][-1]:
            return True 
        # # This needs to be adjusted, or I need to fix choose path
        adj_i, adj_j = self._find_adj_cells(i, j)
    
        # If we haven't visited it we then draw a path
        if not self._cells[adj_i][adj_j].visited:
            self._draw_path(i, j, adj_i, adj_j)
            # and call the next tile adj 
            self._solve_r(adj_i, adj_j)
        # Otherwise we backtrack by 
        # If there is no adj tiles we draw one back, but red
        else:
            prev_i, prev_j = self._find_adj_cells(adj_i, adj_j)
            self._cells[prev_i][prev_j].draw_move(self._cells[adj_i][adj_j], True)
            self._solve_r(prev_i, prev_j)
        # elif self._cells[i][j].visited and self._sum_cell_paths(i, j) < 4:
        #     self._draw_path(i, j)
        # else:
        #     return True
        return False

    def _draw_path(self, i, j, adj_i, adj_j):
        if self._path_wall_stack[(i, j)][0] == 1 and self._path_wall_stack[(adj_i, adj_j)][1] == 1:
            self._path_wall_stack[(i, j)][0] = 0
            self._path_wall_stack[(adj_i, adj_j)][1] = 0
            return self._cells[i][j].draw_move(self._cells[adj_i][adj_j])

        if self._path_wall_stack[(i, j)][1] == 1 and self._path_wall_stack[(adj_i, adj_j)][0] == 1:
            self._path_wall_stack[(i, j)][1] = 0
            self._path_wall_stack[(adj_i, adj_j)][0] = 0
            return self._cells[i][j].draw_move(self._cells[adj_i][adj_j])

        if self._path_wall_stack[(i, j)][2] == 1 and self._path_wall_stack[(adj_i, adj_j)][3] == 1:
            self._path_wall_stack[(i, j)][2] = 0
            self._path_wall_stack[(adj_i, adj_j)][3] = 0
            return self._cells[i][j].draw_move(self._cells[adj_i][adj_j])

        if self._path_wall_stack[(i, j)][3] == 1 and self._path_wall_stack[(adj_i, adj_j)][2] == 1:
            self._path_wall_stack[(i, j)][3] = 0
            self._path_wall_stack[(adj_i, adj_j)][2] = 0
            return self._cells[i][j].draw_move(self._cells[adj_i][adj_j]) 
        return

    def _find_adj_cells(self, i, j):
        # Search Adjacent Members for first 1 
        for cell in self._adj_dict[(i, j)]:
            if not self._cells[cell[0]][cell[1]].visited: 
                if cell[1] < j and i == cell[0] and self._path_wall_stack[(i, j)][0] == 1  and self._path_wall_stack[(cell[0], cell[1])][1] == 1:
                    # Top
                    return cell
                # Bot
                if cell[1] > j and i == cell[0] and self._path_wall_stack[(i, j)][1] == 1  and self._path_wall_stack[(cell[0], cell[1])][0] == 1:
                    return cell
                # Right
                if cell[0] > i and j == cell[1] and self._path_wall_stack[(i, j)][2] == 1  and self._path_wall_stack[(cell[0], cell[1])][3] == 1:
                    return cell
                # Left
                if cell[0] < i and j == cell[1] and self._path_wall_stack[(i, j)][3] == 1  and self._path_wall_stack[(cell[0], cell[1])][2] == 1:
                    return cell
        prev_i, prev_j = self._path_stack.pop()
        return prev_i, prev_j

    def _sum_cell_paths(self, i, j):
        sum = 0
        for x in self._path_wall_stack[(i, j)]:
            sum += x
        return sum

    def _set_list_input(self, i, j):
        directions = [0, 0, 0, 0]
        if not self._cells[i][j].has_top_wall:
            directions[0] = 1
        if not self._cells[i][j].has_bottom_wall:
            directions[1] = 1
        if not self._cells[i][j].has_right_wall:
            directions[2] = 1
        if not self._cells[i][j].has_left_wall:
            directions[3] = 1
        return directions




