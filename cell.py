from line import Line
from point import Point


class Cell:

    def __init__(self, x1: int, x2: int, y1: int, y2: int, window):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._window = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.mid_point = Point(int((x1 + x2) / 2), int((y1 + y2) / 2))

    def draw(self):
        if self.has_left_wall:
            self._window.draw_line(Line(Point(self._x1, self._y1),
                                        Point(self._x1, self._y2)), "black")
        else:
            self._window.draw_line(Line(Point(self._x1, self._y1),
                                        Point(self._x1, self._y2)), "white")

        if self.has_right_wall:
            self._window.draw_line(Line(Point(self._x2, self._y1),
                                        Point(self._x2, self._y2)), "black")
        else:
            self._window.draw_line(Line(Point(self._x2, self._y1),
                                        Point(self._x2, self._y2)), "white")

        if self.has_bottom_wall:
            self._window.draw_line(Line(Point(self._x1, self._y2),
                                        Point(self._x2, self._y2)), "black")
        else:
            self._window.draw_line(Line(Point(self._x1, self._y2),
                                        Point(self._x2, self._y2)), "white")

        if self.has_top_wall:
            self._window.draw_line(Line(Point(self._x1, self._y1),
                                        Point(self._x2, self._y1)), "black")
        else:
            self._window.draw_line(Line(Point(self._x1, self._y1),
                                        Point(self._x2, self._y1)), "white")

    def switch_left(self):
        if self.has_left_wall:
            self.has_left_wall = False
        else:
            self.has_left_wall = True

    def switch_right(self):
        if self.has_right_wall:
            self.has_right_wall = False
        else:
            self.has_right_wall = True

    def switch_top(self):
        if self.has_top_wall:
            self.has_top_wall = False
        else:
            self.has_top_wall = True

    def switch_bot(self):
        if self.has_bottom_wall:
            self.has_bottom_wall = False
        else:
            self.has_bottom_wall = True

    def center(self):
        mid_x = (self._x1 + self._x2) / 2
        mid_y = (self._y1 + self._y2) / 2
        return Point(mid_x, mid_y)

    def draw_move(self, to_cell, undo=False):
        line = Line(self.mid_point, to_cell.mid_point)
        if undo:
            self._window.draw_line(line, "red")
        else:
            self._window.draw_line(line, "gray")
