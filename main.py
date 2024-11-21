import tkinter
import tkinter.ttk as ttk
from tkinter import DISABLED, NORMAL
import canvas_helpers

CANVAS_DIMENSIONS = 500


window = tkinter.Tk()
form = ttk.Frame(window, padding=10)
form.grid()
ttk.Label(form, text="Hello World!").grid(column=0, row=0)


canvas = tkinter.Canvas(
    form, bg="white", bd=10, width=CANVAS_DIMENSIONS, height=CANVAS_DIMENSIONS
)
canvas.grid(column=0, row=1, rowspan=10)

ttk.Separator(form, orient="vertical").grid(column=1, row=0, rowspan=10)

wrapper = canvas_helpers.canvasWrapper(canvas)


def _graham_iterate():
    if not canvas_helpers.graham_step(wrapper):
        canvas.after(100, _graham_iterate)


def random_points():
    canvas_helpers.random_points(wrapper)


    one_step_button.config(state=NORMAL)
    animate_scan_button.config(state=NORMAL)
    do_graham_scan_button.config(state=NORMAL)

def animate():
    _graham_iterate()
    add_points_button.config(state=DISABLED)
    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)

def step():
    add_points_button.config(state=DISABLED)
    if canvas_helpers.graham_step(wrapper):
        one_step_button.config(state=DISABLED)
        animate_scan_button.config(state=DISABLED)
        do_graham_scan_button.config(state=DISABLED)

def clear():
    canvas_helpers.clear_canvas(wrapper)
    add_points_button.config(state=NORMAL)

    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)

    
def scan():
    canvas_helpers.graham_result(wrapper)
    add_points_button.config(state=DISABLED)
    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)

def initial_state():
        
    add_points_button.config(state=NORMAL)
    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)

add_points_button = ttk.Button(
    form,
    text="Add random points",
    command=random_points,
)
add_points_button.grid(column=2, row=1)

do_graham_scan_button = ttk.Button(
    form,
    text="Graham Scan",
    command=scan,
)
do_graham_scan_button.grid(column=2, row=2)

animate_scan_button = ttk.Button(form, text="Animate Graham Sort", command=animate)

animate_scan_button.grid(
    column=2, row=3
)

one_step_button = ttk.Button(
    form, text="Do 1 step", command=step
)
one_step_button.grid(column=2, row=4)

clear_button = ttk.Button(
    form, text="Clear canvas", command=clear
)
clear_button.grid(column=2, row=5)


ttk.Button(form, text="Quit", command=window.destroy).grid(column=2, row=10)





initial_state()
window.mainloop()
