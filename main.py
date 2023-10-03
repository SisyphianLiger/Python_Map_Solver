from point import Point
from line import Line
from window import Window


def main():
    win = Window(800, 600)
    p1, p2 = Point(50, 100), Point(0, 600)
    line = Line(p1, p2)
    win.draw_line(line, "red")
    win.wait_for_close()


main()

