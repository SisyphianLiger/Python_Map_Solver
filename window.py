from tkinter import Tk, BOTH, Canvas


class Window:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root_widget = Tk()
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.root_widget.update()
        self.root_widget.update_idletasks()

    def wait_for_close(self):
        self.running = True
        if self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.root_widget.protocol()
