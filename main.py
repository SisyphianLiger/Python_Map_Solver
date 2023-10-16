from window import Window
from maze import Maze
import sys

def main():
    sys.setrecursionlimit(100000)
    win = Window(2400, 1200)
    Maze(100, 25, 100, 100, 10, 10, win)
    win.wait_for_close()


main()
