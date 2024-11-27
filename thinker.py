"""
Thinker based GUI quickhull game board.

@author James Ford
"""
import tkinter as tk
import quickhull


def screen_to_math(x: int, y: int):
    """
    Calculate the math coordinate of the point based on screen coordinate.
    :param x: X-axis screen coordinate.
    :param y: Y-axis screen coordinate.
    :return: tuple of math coordinate of the point.
    """
    return (x - 250) / 12.5, (250 - y) / 12.5


def math_to_screen(x: int, y: int):
    """
    Calculate the screen coordinate of the point based on math coordinate.
    :param x: X-axis math coordinate.
    :param y: Y-axis math coordinate.
    :return: tuple of math coordinate of the point.
    """
    return x * 12.5 + 250, 250 - y * 12.5


def draw_grid():
    """
    Create grid and XY axis on the canvas.
    :return: None
    """
    for i in range(0, 501, 25):
        CANVAS.create_line(i, 0, i, 500, fill="lightgrey")
        CANVAS.create_line(0, i, 500, i, fill="lightgrey")
    CANVAS.create_line(250, 0, 250, 500, fill="black", width=2)
    CANVAS.create_line(0, 250, 500, 250, fill="black", width=2)


def user_plot(event: tk.Event):
    """
    Create oval point with coordinate label when user plot on canvas and store the coordinate.
    :param event: Thinker event listener.
    :return: None
    """
    point = screen_to_math(round(event.x / 25) * 25, round(event.y / 25) * 25)
    # Prevent user create multiple point on same coordinate.
    if point not in POINTS:
        POINTS.append(point)
        plot_point(point, label=True, fill="red")
        update_point_count()


def plot_point(point: tuple, size=5, label=False, **kwargs):
    """
    Create oval point on canvas.
    :param point: Point (x, y) coordinate in tuple.
    :param size: Size of the point oval.
    :param label: Whether display coordinate label, default is not.
    :param kwargs: Additional keyword arguments for 'create_oval'.
    :return:
    """
    screen_x, screen_y = math_to_screen(*point)
    CANVAS.create_oval(screen_x - size, screen_y - size, screen_x + size, screen_y + size, **kwargs)
    if label:
        CANVAS.create_text(screen_x, screen_y + 10, text="({:.0f}, {:.0f})".format(*point))


def line_point(point_a: tuple, point_b: tuple, fill="grey", width=2, **kwargs):
    """
    Create a line connect two points on canvas.
    :param point_a: Point A (x, y) coordinate in tuple.
    :param point_b: Point B (x, y) coordinate in tuple.
    :param fill: Colour of the line.
    :param width:  Width of the line
    :param kwargs: Additional keyword arguments for 'create_line'.
    :return:
    """
    screen_point_a = math_to_screen(*point_a)
    screen_point_b = math_to_screen(*point_b)
    CANVAS.create_line(*screen_point_a, *screen_point_b, fill=fill, width=width, **kwargs)


def toggle_drawing(enabled: bool):
    """
    Enable or disable user plot ability.
    :param enabled: True/False for enable or disable.
    :return: None
    """
    if enabled:
        CANVAS.bind("<Button-1>", user_plot)
    else:
        CANVAS.unbind("<Button-1>")


def toggle_button(button: tk.Button, enable: bool):
    """
    Enable or disable thinker button.
    :param button: Thinker button object.
    :param enable: True/False for enable or disable.
    :return: None
    """
    if enable:
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)


def update_point_count():
    """
    Update point count text of the label.
    :return: None
    """
    POINT_COUNT_LABEL.config(text=f"Points: {len(POINTS)}")


def calculate_convex_hull():
    """
    Calculate convex hull with quickhull and display on canvas.
    :return: None
    """
    if len(POINTS) >= 3:
        toggle_drawing(False)
        toggle_button(CALCULATE_CONVEX_HULL_BUTTON, False)
        toggle_button(SHOW_STEPS_BUTTON, True)
        global CONVEX_HULL_DATA
        CONVEX_HULL_DATA = quickhull.quick_hull(POINTS)
        for i in range(len(CONVEX_HULL_DATA[0])):
            point_a = CONVEX_HULL_DATA[0][i]
            point_b = CONVEX_HULL_DATA[0][(i + 1) % len(CONVEX_HULL_DATA[0])]
            line_point(point_a, point_b)
            plot_point(point_a, fill="green", size=6)


def show_steps():
    """
    Demonstrate each step of choose quick hull point.
    :return: None
    """
    def show_step(points):
        """
        Display the convex hull of the specific step.
        :param points: List of points for the step.
        :return: None
        """
        CANVAS.delete("steps")
        step_hull = quickhull.quick_hull(points)[0]
        for i in range(len(step_hull)):
            point_a = step_hull[i]
            point_b = step_hull[(i + 1) % len(step_hull)]
            line_point(point_a, point_b, fill="orange", tags="steps")
            plot_point(point_a, fill="lightgreen", size=6, tags="step")

    if CONVEX_HULL_DATA:
        toggle_button(RESET_BUTTON, False)
        CANVAS.delete("steps")
        steps = len(CONVEX_HULL_DATA[1])
        for i in range(steps):
            ROOT.after(i * 500, lambda i=i: show_step(CONVEX_HULL_DATA[1][:i + 1]))
        ROOT.after(steps * 500, lambda: toggle_button(RESET_BUTTON, True))


def reset_canvas():
    """
    Reset the entire canvas.
    :return: None
    """
    CANVAS.delete("all")
    POINTS.clear()
    draw_grid()
    update_point_count()
    toggle_button(CALCULATE_CONVEX_HULL_BUTTON, True)
    toggle_button(SHOW_STEPS_BUTTON, False)
    toggle_drawing(True)


def initial():
    """
    Initial the canvas.
    :return: None
    """
    draw_grid()
    toggle_drawing(True)
    toggle_button(SHOW_STEPS_BUTTON, False)
    ROOT.mainloop()


if __name__ == "__main__":
    print("[QuickHull Board] Initializing...")
    POINTS = []
    CONVEX_HULL_DATA = None

    ROOT = tk.Tk()
    ROOT.title("QuickHull Board")

    CANVAS = tk.Canvas(ROOT, width=500, height=500)
    CANVAS.grid(row=0, column=0, columnspan=3)

    POINT_COUNT_LABEL = tk.Label(ROOT, text="Points: 0")
    POINT_COUNT_LABEL.grid(row=1, column=0, columnspan=3)

    RESET_BUTTON = tk.Button(ROOT, text="Reset", command=reset_canvas)
    RESET_BUTTON.grid(row=2, column=0, padx=5, pady=5)

    CALCULATE_CONVEX_HULL_BUTTON = tk.Button(ROOT, text="Calculate Convex Hull", command=calculate_convex_hull)
    CALCULATE_CONVEX_HULL_BUTTON.grid(row=2, column=1, padx=5, pady=5)

    SHOW_STEPS_BUTTON = tk.Button(ROOT, text="Show Steps", command=show_steps)
    SHOW_STEPS_BUTTON.grid(row=2, column=2, padx=5, pady=5)

    print("[QuickHull Board] Running GUI...")
    initial()
