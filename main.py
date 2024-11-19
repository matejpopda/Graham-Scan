import tkinter
import tkinter.ttk as ttk

import canvas_helpers

CANVAS_DIMENSIONS = 500


window = tkinter.Tk()
form =  ttk.Frame(window, padding = 10)
form.grid()
ttk.Label(form, text="Hello World!").grid(column=0, row=0)


canvas = tkinter.Canvas(form, bg="white", bd=10, width=CANVAS_DIMENSIONS, height=CANVAS_DIMENSIONS)
canvas.grid(column=0, row=1, rowspan=10)

ttk.Separator(form, orient="vertical").grid(column=1, row=0, rowspan=10)

wrapper = canvas_helpers.canvasWrapper(canvas)

ttk.Button(form, text="Add random points", command=lambda: canvas_helpers.random_points(wrapper)).grid(column=2, row=1)
ttk.Button(form, text="Convex Hull", command=lambda: canvas_helpers.graham_result(wrapper)).grid(column=2, row=2)
ttk.Button(form, text="Run Graham Sort", command=lambda: canvas_helpers.graham_iterate(wrapper)).grid(column=2, row=3)
ttk.Button(form, text="Step through", command=lambda: canvas_helpers.graham_step(wrapper)).grid(column=2, row=4)
ttk.Button(form, text="Clear canvas", command=lambda: canvas_helpers.clear_canvas(wrapper)).grid(column=2, row=5)
ttk.Button(form, text="Quit", command=window.destroy).grid(column=2, row=6)









window.mainloop()