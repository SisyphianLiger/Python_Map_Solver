from window import Window
from cell import Cell


def main():
    win = Window(800, 600)
    cell1 = Cell(200, 300, 200, 300, win)
    cell2 = Cell(400, 500, 400, 500, win)
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2, True)
    win.wait_for_close()


main()

