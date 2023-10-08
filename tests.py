import unittest
from maze import Maze
from window import Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        win = Window(800, 600)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(m1._cells),
            num_cols * num_rows,
        )

    def good_entrance_exit(self):
        num_cols = 10
        num_rows = 10
        win = Window(800, 600)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            m1._cells[0].has_left_wall(),
            False,
        )
        self.assertEqual(
            m1._cells[-1].has_right_wall(),
            False,
        )


if __name__ == "__main__":
    unittest.main()
