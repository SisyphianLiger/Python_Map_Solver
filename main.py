from window import Window
from maze import Maze


def main():
    win = Window(600, 600)
    maze = Maze(50, 50, 20, 20, 25, 25, win)
    maze.solve()
    win.wait_for_close()


main()
