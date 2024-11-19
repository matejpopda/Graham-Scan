import tkinter
import time
import typing
import dataclasses
import random

POINT_SIZE = 5


@dataclasses.dataclass
class Point:
    x:float
    y:float
    
@dataclasses.dataclass
class Line:
    a:Point
    b:Point
    

class canvasWrapper:
    def __init__(self, canvas: tkinter.Canvas) -> None:
        self.canvas: tkinter.Canvas = canvas
        self.points: list[Point] = []
        self.current_boundary: list[Line] = []
        self.lines_on_stack: list[Line] = []
        self.removed_lines: list[Line] = []
    
    def draw(self):
        self.canvas.delete("all")

        for point in self.points:
            size = POINT_SIZE/2
            self.canvas.create_oval(point.x - size, point.y - size, point.x + size, point.y + size)

        for line in self.current_boundary:
            self.canvas.create_line(line.a.x, line.a.y, line.b.x, line.b.y, dash=(1,0), fill="black")

        for line in self.lines_on_stack:
            self.canvas.create_line(line.a.x, line.a.y, line.b.x, line.b.y, dash=(1,0), fill="green")

        for line in self.removed_lines:
            self.canvas.create_line(line.a.x, line.a.y, line.b.x, line.b.y, dash=(1,2), fill="red")




def clear_canvas(canvas: canvasWrapper):
    canvas.points = []
    canvas.current_boundary = []
    canvas.lines_on_stack = []
    canvas.removed_lines = []
    canvas.draw()



def random_points(canvas: canvasWrapper):
    boundaryx = canvas.canvas.winfo_reqwidth()
    boundaryy = canvas.canvas.winfo_reqheight()

    for _ in range(10):
        x = random.uniform(0, boundaryx)
        y = random.uniform(0, boundaryy)

        canvas.points.append(Point(x,y))

    canvas.draw()



def graham_step(canvas: canvasWrapper) -> bool:
    pass


def graham_iterate(canvas: canvasWrapper):
    while graham_step(canvas):
        time.sleep(0.1)


def graham_result(canvas: canvasWrapper):
    while graham_step(canvas):
        pass



def convex_hull(canvas: canvasWrapper):
    pass
