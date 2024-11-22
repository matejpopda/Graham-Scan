import tkinter
import tkinter.ttk as ttk
from tkinter.font import Font
from tkinter import DISABLED, NORMAL
import canvas_helpers
import tkinter.font as tkFont


CANVAS_DIMENSIONS = 500


window = tkinter.Tk()



how_many_random_points = tkinter.IntVar(value='10')
animation_delay = tkinter.IntVar(value='100')
enumeration = tkinter.BooleanVar(value=False)





form = ttk.Frame(window, padding=10)
form.grid()
ttk.Label(form, text="Click to Add Points!").grid(column=0, row=0)


canvas = tkinter.Canvas(
    form, bg="white", bd=10, width=CANVAS_DIMENSIONS, height=CANVAS_DIMENSIONS
)
canvas.grid(column=0, row=1, rowspan=10)

ttk.Separator(form, orient="vertical").grid(column=1, row=0, rowspan=10)

wrapper = canvas_helpers.canvasWrapper(canvas)


def _graham_iterate():
    if not canvas_helpers.graham_step(wrapper):
        canvas.after(animation_delay.get(), _graham_iterate)


def random_points():
    canvas_helpers.random_points(wrapper, how_many_random_points.get())


    one_step_button.config(state=NORMAL)
    animate_scan_button.config(state=NORMAL)
    do_graham_scan_button.config(state=NORMAL)

def animate():
    _graham_iterate()
    add_points_button.config(state=DISABLED)
    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)
    wrapper.allow_click_input = False

def step():
    add_points_button.config(state=DISABLED)
    wrapper.allow_click_input = False
    if canvas_helpers.graham_step(wrapper):
        one_step_button.config(state=DISABLED)
        animate_scan_button.config(state=DISABLED)
        do_graham_scan_button.config(state=DISABLED)

def clear():
    canvas_helpers.clear_canvas(wrapper)
    add_points_button.config(state=NORMAL)
    wrapper.allow_click_input = True
    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)

    
def scan():
    canvas_helpers.graham_result(wrapper)
    add_points_button.config(state=DISABLED)
    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)
    wrapper.allow_click_input = False

def initial_state():
    wrapper.allow_click_input = True
    add_points_button.config(state=NORMAL)
    one_step_button.config(state=DISABLED)
    animate_scan_button.config(state=DISABLED)
    do_graham_scan_button.config(state=DISABLED)

def on_click(event):

    if not wrapper.allow_click_input:
        return

    canvas_helpers.point_at_coords(wrapper, event.x, event.y)

    if len(wrapper.points) < 2 or len(wrapper.lines_on_stack) > 0:
        return
    
    one_step_button.config(state=NORMAL)
    animate_scan_button.config(state=NORMAL)
    do_graham_scan_button.config(state=NORMAL)

def enumerate_points():
    wrapper.do_enumeration = enumeration.get()
    wrapper.draw()

def clear_lines():
    canvas_helpers.clear_canvas(wrapper,True)

    add_points_button.config(state=NORMAL)
    wrapper.allow_click_input = True

    if len(wrapper.points) < 2: 
        return
    
    one_step_button.config(state=NORMAL)
    animate_scan_button.config(state=NORMAL)
    do_graham_scan_button.config(state=NORMAL)






add_points_button = ttk.Button(
    form,
    text="Add random points",
    command=random_points,
)
add_points_button.grid(column=2, row=1)


random_settings_spinbox = ttk.Spinbox(form,from_=2, to=100, increment=5, textvariable=how_many_random_points, width=5)
random_settings_spinbox.grid(column=2, row=2)

do_graham_scan_button = ttk.Button(
    form,
    text="Graham Scan",
    command=scan,
)
do_graham_scan_button.grid(column=2, row=3)

animate_scan_button = ttk.Button(form, text="Animate Graham Sort", command=animate)
animate_scan_button.grid(
    column=2, row=4
)

animate_settings_spinbox = ttk.Spinbox(form,from_=1, to=1000, increment=100, textvariable=animation_delay, width=5)
animate_settings_spinbox.grid(column=2, row=5)


one_step_button = ttk.Button(
    form, text="Do 1 step", command=step
)
one_step_button.grid(column=2, row=6)

enumerate_button = ttk.Checkbutton(
    form, text="Enumerate Points According to \nhow they are in the array", command=enumerate_points, variable=enumeration
)

enumerate_button.grid(column=2, row=7)



clear_button = ttk.Button(
    form, text="Clear lines", command=clear_lines
)
clear_button.grid(column=2, row=8)

clear_button = ttk.Button(
    form, text="Clear canvas", command=clear
)
clear_button.grid(column=2, row=9)



ttk.Button(form, text="Quit", command=window.destroy).grid(column=2, row=10)



canvas.bind("<Button-1>", on_click)


initial_state()
window.mainloop()
