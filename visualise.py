"""
Tkinter for QuickHull visualization

@Author James Ford
"""

import tkinter as tk
from tkinter import ttk
import random
import quickhull


# Helper functions for coordinate conversions
def screen_to_math(x: int, y: int):
    """
    Calculate the math coordinate of the point based on screen coordinate.
    :param x: X-axis screen coordinate.
    :param y: Y-axis screen coordinate.
    :return: tuple of math coordinate of the point.
    """
    return (x - CANVAS_WIDTH / 2) / SCALE, (CANVAS_HEIGHT / 2 - y) / SCALE


def math_to_screen(x: int, y: int):
    """
    Calculate the screen coordinate of the point based on math coordinate.
    :param x: X-axis math coordinate.
    :param y: Y-axis math coordinate.
    :return: tuple of math coordinate of the point.
    """
    return x * SCALE + CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - y * SCALE


# Function to draw grid and axes
def draw_grid():
    """
    Create grid and XY axis on the canvas.
    :return: None
    """
    CANVAS.delete("grid")
    for i in range(0, CANVAS_WIDTH, GRID_SPACING):
        CANVAS.create_line(i, 0, i, CANVAS_HEIGHT, fill="lightgrey", tags="grid")
    for i in range(0, CANVAS_HEIGHT, GRID_SPACING):
        CANVAS.create_line(0, i, CANVAS_WIDTH, i, fill="lightgrey", tags="grid")
    CANVAS.create_line(CANVAS_WIDTH / 2, 0, CANVAS_WIDTH / 2, CANVAS_HEIGHT, fill="#3B3B3B", width=2, tags="grid")
    CANVAS.create_line(0, CANVAS_HEIGHT / 2, CANVAS_WIDTH, CANVAS_HEIGHT / 2, fill="#3B3B3B", width=2, tags="grid")


# Adjust canvas size dynamically
def resize_canvas(event):
    """
    Used to scale the points and canvas when adjusted by the user
    :param event: Thinker event listener.
    """
    global CANVAS_WIDTH, CANVAS_HEIGHT, SCALE
    CANVAS_WIDTH, CANVAS_HEIGHT = event.width, event.height
    SCALE = min(CANVAS_WIDTH, CANVAS_HEIGHT) / 50  # Adjust scale dynamically
    draw_grid()
    redraw_points_and_hull()


def redraw_points_and_hull():
    """
    Redraw all points and the convex hull when the canvas is resized.
    """
    CANVAS.delete("all")
    draw_grid()
    for point in POINTS:
        plot_point(point, size=6, fill="#FF5252", label=True)
    if CONVEX_HULL_DATA:
        calculate_convex_hull()


# Plot a point on the canvas
def plot_point(point, size=5, label=False, **kwargs):
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
        CANVAS.create_text(screen_x, screen_y + 15, text=f"({point[0]:.1f}, {point[1]:.1f})", fill="#5A5A5A", tags="points")


# Draw a polygon connecting points
def draw_polygon(points, color, width=2, tags="polygon"):
    """
    Used to draw the convex hull on the canvas
    :param points: set of points making up the polygon
    :param colour: colour of the polygon
    :param width: the width of the lines to use to create the polygon
    :param tags: used to keep track of the points that make up the polygons
    """
    for i in range(len(points)):
        line_point(points[i], points[(i + 1) % len(points)], fill=color, width=width, tags=tags)


# Draw a line between two points
def line_point(point_a, point_b, **kwargs):
    """
    Create a line connect two points on canvas.
    :param point_a: Point A (x, y) coordinate in tuple.
    :param point_b: Point B (x, y) coordinate in tuple.
    :param kwargs: Additional keyword arguments for 'create_line'.
    :return:
    """
    screen_a = math_to_screen(*point_a)
    screen_b = math_to_screen(*point_b)
    CANVAS.create_line(*screen_a, *screen_b, **kwargs)


# Add user plot
def user_plot(event):
    """
    Create oval point with coordinate label where the user clicks on the canvas.
    :param event: Thinker event listener.
    :return: None
    """
    math_point = screen_to_math(event.x, event.y)
    snapped_point = (round(math_point[0], 1), round(math_point[1], 1))
    if snapped_point not in POINTS:
        POINTS.append(snapped_point)
        plot_point(snapped_point, size=6, fill="#FF5252", label=True, tags="user-point")
        update_point_count()


def update_point_count():
    """
    Update the point count to reflect points on the canvas
    """
    POINT_COUNT_LABEL.config(text=f"Points: {len(POINTS)}")


def reset_canvas():
    """
    Reset the entire canvas.
    :return: None
    """
    CANVAS.delete("all")
    POINTS.clear()
    draw_grid()
    update_point_count()
    toggle_buttons(state="normal")
    global CONVEX_HULL_DATA
    CONVEX_HULL_DATA = None



def calculate_convex_hull():
    """
    Calculate convex hull with quickhull and display on canvas.
    :return: None
    """
    if len(POINTS) < 2:
        return
    global CONVEX_HULL_DATA
    CANVAS.delete("hull")
    CONVEX_HULL_DATA = quickhull.quick_hull(POINTS)
    hull = CONVEX_HULL_DATA[0]
    draw_polygon(hull, color="#0078D4", width=2, tags="hull")
    for point in hull:
        plot_point(point, size=7, fill="#00C853", tags="hull")
    BUTTONS["steps-button"].config(state=tk.NORMAL)


# Show iterative steps of the QuickHull algorithm
def show_steps():
    """
    Demonstrate the steps for computing the convexhull
    :return: None
    """
    if CONVEX_HULL_DATA is None:
        return
    
    steps = CONVEX_HULL_DATA[1]
    CANVAS.delete("steps")
    toggle_buttons(state=tk.DISABLED)

    def visualize_step(i):
        """
        Display the convex hull of the specific step.
        :param points: List of points for the step.
        :return: None
        """
        CANVAS.delete("steps")
        step_points = steps[:i + 1]
        step_hull = quickhull.quick_hull(step_points)[0]
        draw_polygon(step_hull, color="orange", tags="steps")
        for point in step_hull:
            plot_point(point, size=6, fill="lightgreen", tags="steps")

    for i in range(len(steps)):
        ROOT.after(i * 500, lambda i=i: visualize_step(i))

    ROOT.after(len(steps) * 500, lambda: toggle_buttons(state="normal"))


# Optimized layer peeling
def peel_layers():
    """
    Iterately calls the quick_hull algorithm and visualises the convex hulls at each layer 
    """
    CANVAS.delete("peel")
    points = POINTS[:]
    layer_colors = ["#FFC107", "#4CAF50", "#FF5722", "#03A9F4", "#673AB7"]
    layer_index = 0

    if not points:
        return

    while points:
        hull = quickhull.quick_hull(points)[0]
        if not hull:
            break
        draw_polygon(hull, color=layer_colors[layer_index % len(layer_colors)], width=2, tags="peel")
        for point in hull:
            plot_point(point, size=7, fill=layer_colors[layer_index % len(layer_colors)], tags="peel")
        points = [p for p in points if p not in hull]
        layer_index += 1


# Generate random points
def generate_random_points(num_points=20):
    """
    Generate a random set of points on the graph
    : param  num_points: The number of points to randomly place on the canvas
    """
    reset_canvas()
    for _ in range(num_points):
        random_x = round(random.uniform(-CANVAS_WIDTH / (2 * SCALE), CANVAS_WIDTH / (2 * SCALE)), 1)
        random_y = round(random.uniform(-CANVAS_HEIGHT / (2 * SCALE), CANVAS_HEIGHT / (2 * SCALE)), 1)
        POINTS.append((random_x, random_y))
        plot_point((random_x, random_y), size=6, fill="#FF5252", label=True, tags="user-point")
    update_point_count()


def toggle_buttons(state, exclude=[]):
    """
    Switch the state of buttons on the canvas 
    : param state: The state you want the buttons to be in
    : param exclude: The buttons to be excluded
    """
    for button_id, button in BUTTONS.items():
        if button_id not in exclude:
            button.config(state=state)


# Initialization
if __name__ == "__main__":
    CANVAS_WIDTH, CANVAS_HEIGHT = 600, 600
    GRID_SPACING, SCALE = 25, 12.5
    POINTS = []
    CONVEX_HULL_DATA = None

    ROOT = tk.Tk()
    ROOT.title("QuickHull Visualization")
    ROOT.configure(bg="#2E2E2E")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", padding=4, font=("Arial", 12), foreground="#FFFFFF", background="#80669d")
    style.configure("TLabel", font=("Arial", 12), foreground="#FFFFFF", background="#2E2E2E")

    CANVAS = tk.Canvas(ROOT, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#F4F4F4", highlightthickness=0)
    CANVAS.grid(row=0, column=0, columnspan=5, sticky="nsew")
    CANVAS.bind("<Button-1>", user_plot)
    CANVAS.bind("<Configure>", resize_canvas)

    ROOT.rowconfigure(0, weight=1)
    ROOT.columnconfigure(0, weight=1)

    POINT_COUNT_LABEL = ttk.Label(ROOT, text="Points: 0")
    POINT_COUNT_LABEL.grid(row=1, column=0, columnspan=5)

    BUTTONS = {
        "reset-button": ttk.Button(ROOT, text="Reset", command=reset_canvas),
        "calculate-button": ttk.Button(ROOT, text="Calculate Convex Hull", command=calculate_convex_hull),
        "steps-button": ttk.Button(ROOT, text="Show Steps", command=show_steps, state=tk.DISABLED),
        "layers-button": ttk.Button(ROOT, text="Peel Layers", command=peel_layers),
        "random-button": ttk.Button(ROOT, text="Generate Random Points", command=lambda: generate_random_points(random.randint(15,70))),
    }

    for i, button in enumerate(BUTTONS.values()):
        button.grid(row=2, column=i)

    draw_grid()
    ROOT.mainloop()
