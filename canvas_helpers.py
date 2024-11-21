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
        self.sorted: bool = False
        self.position: int = 0
        self.lowest_point: Point|None = None
    
    def draw(self):
        self.canvas.delete("all")

        def transform_y_coord(y):
            return  y 
            return self.canvas.winfo_reqheight() - y 

        def draw_line(line: Line, dash=(1), fill="black"):
            self.canvas.create_line(line.a.x, 
                                    transform_y_coord(line.a.y), 
                                    line.b.x, 
                                    transform_y_coord(line.b.y), 
                                    dash=dash, 
                                    fill=fill)

        def draw_point(point: Point, size):
            x = point.x
            y = transform_y_coord(point.y)

            self.canvas.create_oval(x - size, 
                                    y - size, 
                                    x + size, 
                                    y + size)

        for i in range(len(self.points)):
            point = self.points[i]
            size = POINT_SIZE/2 * (i+1)
            draw_point(point, size)

        for line in self.current_boundary:
            draw_line(line)

        for line in self.lines_on_stack:
            draw_line(line, dash=(1), fill='green')

        for line in self.removed_lines:
            draw_line(line, dash=(1,2), fill="red")


def clear_canvas(canvas: canvasWrapper):
    canvas.points = []
    canvas.current_boundary = []
    canvas.lines_on_stack = []
    canvas.removed_lines = []
    canvas.draw()
    canvas.sorted = False
    canvas.lowest_point = None
    canvas.position = 0



def random_points(canvas: canvasWrapper):
    boundaryx = canvas.canvas.winfo_reqwidth()
    boundaryy = canvas.canvas.winfo_reqheight()

    for _ in range(10):
        x = random.uniform(boundaryx*0.2, boundaryx*0.8)
        y = random.uniform(boundaryy*0.2, boundaryy*0.8)

        canvas.points.append(Point(x,y))

    canvas.draw()



def graham_step_no_draw(canvas: canvasWrapper) -> bool:
    if not canvas.sorted:
        find_lowest_point(canvas)
        def sorter(point: Point):
            if canvas.lowest_point == point:
                return -100
            x = point.x - canvas.lowest_point.x
            y = point.y - canvas.lowest_point.y
            res = (1 * x + 0 * y)/((1)*(pow(x*x+y*y, 1/2)))
            # print(res)
            return res 
            
        canvas.points.sort(key=sorter, reverse=False)
        canvas.sorted = True
        canvas.position = 2

        canvas.lines_on_stack.append(Line(canvas.points[0], canvas.points[1]))
        return False


    if canvas.position == len(canvas.points):
        canvas.lines_on_stack.append(Line(canvas.points[-1], canvas.points[0]))
        return True    
    
    if canvas.position > len(canvas.points)- 1 :
        return True

    current_point = canvas.points[canvas.position]

    canvas.lines_on_stack.append(Line(canvas.lines_on_stack[-1].b, current_point))



    if cross_product(canvas.lines_on_stack[-2], canvas.lines_on_stack[-1]) > 0:
        canvas.removed_lines.append(canvas.lines_on_stack.pop())
        canvas.removed_lines.append(canvas.lines_on_stack.pop())
        return False

    canvas.position += 1 
    
    return False

def cross_product(line1:Line, line2:Line):
    assert line1.b == line2.a 

    return (line1.b.x - line1.a.x)*(line2.b.y - line1.a.y) - (line1.b.y - line1.a.y)*(line2.b.x - line1.a.x)
    
       

    


        

def find_lowest_point(canvas: canvasWrapper) -> None:
    lowest = canvas.points[0]

    for i in canvas.points:
        if i.y < lowest.y:
            lowest = i

    canvas.lowest_point= lowest

def graham_step(canvas: canvasWrapper) -> bool:
    x = graham_step_no_draw(canvas)
    canvas.draw()
    return x 



def graham_result(canvas: canvasWrapper):
    while not graham_step_no_draw(canvas):
        pass
    canvas.draw()


