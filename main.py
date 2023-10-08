from window import Window
from maze import Maze


def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 3, 3, 100, 100, win)
    win.wait_for_close()


main()

