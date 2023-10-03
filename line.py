from point import Point
from tkinter import Canvas, BOTH


class Line:

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color="red"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y,
                           fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)
