import tkinter
import time
import typing
import dataclasses
import random

POINT_SIZE = 20


@dataclasses.dataclass
class Point:
    x: float
    y: float


@dataclasses.dataclass
class Line:
    a: Point
    b: Point


class canvasWrapper:
    def __init__(self, canvas: tkinter.Canvas) -> None:
        self.canvas: tkinter.Canvas = canvas
        self.points: list[Point] = []
        self.current_boundary: list[Line] = []
        self.lines_on_stack: list[Line] = []
        self.removed_lines: list[Line] = []
        self.sorted: bool = False
        self.position: int = 0
        self.lowest_point: Point | None = None
        self.do_enumeration: bool = False
        self.allow_click_input = True

    def add_point(self, point:Point):
        for i in self.points:
            if i.x == point.x and i.y == point.y:
                return
        self.points.append(point)
        

    


    def draw(self):
        self.canvas.delete("all")

        def draw_line(line: Line, dash=(1), fill="black", width=7):
            self.canvas.create_line(
                line.a.x,
                line.a.y,
                line.b.x,
                line.b.y,
                dash=dash,
                fill=fill,
                width=width
            )

        def draw_point(point: Point, size, number_to_print):
            x = point.x
            y = point.y

            self.canvas.create_oval(x - size, y - size, x + size, y + size)

            if self.do_enumeration:
                self.canvas.create_text(x,y, text=number_to_print)

        for i in range(len(self.points)):
            point = self.points[i]
            size = POINT_SIZE / 2
            draw_point(point, size, i)

        for line in self.current_boundary:
            draw_line(line, dash=None)

        for line in self.removed_lines:
            draw_line(line, dash=(1, 2), fill="red", width=3)

        for line in self.lines_on_stack:
            draw_line(line, dash=(1), fill="green", width=5)



def clear_canvas(canvas: canvasWrapper, keep_points=False):
    if not keep_points:
        canvas.points = []
    canvas.current_boundary = []
    canvas.lines_on_stack = []
    canvas.removed_lines = []
    canvas.draw()
    canvas.sorted = False
    canvas.lowest_point = None
    canvas.position = 0


def random_points(canvas: canvasWrapper, how_many):
    boundaryx = canvas.canvas.winfo_reqwidth()
    boundaryy = canvas.canvas.winfo_reqheight()

    for _ in range(how_many):
        x = int(random.uniform(boundaryx * 0.1, boundaryx * 0.9))
        y = int(random.uniform(boundaryy * 0.1, boundaryy * 0.9))

        canvas.add_point(Point(x, y))

    canvas.draw()

def point_at_coords(canvas: canvasWrapper, x, y):
    canvas.add_point(Point(x,y))
    canvas.draw()


def graham_step_no_draw(canvas: canvasWrapper) -> bool:
    if not canvas.sorted:
        find_lowest_point(canvas)

        def sorter(point: Point):
            if canvas.lowest_point == point:
                return 100
            x = point.x - canvas.lowest_point.x
            y = point.y - canvas.lowest_point.y
            res = (1 * x + 0 * y) / ((1) * (pow(x * x + y * y, 1 / 2)))
            # print(res)
            return res

        canvas.points.sort(key=sorter, reverse=True)
        canvas.sorted = True
        canvas.position = 2

        canvas.lines_on_stack.append(Line(canvas.points[0], canvas.points[1]))
        return False

    if canvas.position == len(canvas.points):
        canvas.lines_on_stack.append(Line(canvas.points[-1], canvas.points[0]))

        canvas.current_boundary = canvas.lines_on_stack.copy()
        return True

    if canvas.position > len(canvas.points) - 1:
        return True

    current_point = canvas.points[canvas.position]

    canvas.lines_on_stack.append(Line(canvas.lines_on_stack[-1].b, current_point))

    if cross_product(canvas.lines_on_stack[-2], canvas.lines_on_stack[-1]) > 0:
        canvas.removed_lines.append(canvas.lines_on_stack.pop())
        canvas.removed_lines.append(canvas.lines_on_stack.pop())
        return False

    canvas.position += 1

    return False


def cross_product(line1: Line, line2: Line):
    assert line1.b == line2.a

    return (line1.b.x - line1.a.x) * (line2.b.y - line1.a.y) - (
        line1.b.y - line1.a.y
    ) * (line2.b.x - line1.a.x)


# Actually finds the highest because the coordinate system is reversed
def find_lowest_point(canvas: canvasWrapper) -> None:
    lowest = canvas.points[0]

    for i in canvas.points:
        if i.y > lowest.y:
            lowest = i

    canvas.lowest_point = lowest


def graham_step(canvas: canvasWrapper) -> bool:
    x = graham_step_no_draw(canvas)
    canvas.draw()
    return x


def graham_result(canvas: canvasWrapper):
    while not graham_step_no_draw(canvas):
        pass
    canvas.draw()
