"""
Tkinter for QuickHull visualization

@Author James Ford
"""

import tkinter as tk
from tkinter import ttk
import random
import quickhull


# --- Helper Functions for Coordinate Conversions ---

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


# --- Functions for Drawing and Interaction ---

def draw_grid():
    """
    Draw the gridlines and the X/Y axis on the canvas 
    :return: None
    """

    # Clear any existing grid first
    CANVAS.delete("grid")
    
    # Draw vertical and horizontal grid lines
    for i in range(0, CANVAS_WIDTH, GRID_SPACING):
        CANVAS.create_line(i, 0, i, CANVAS_HEIGHT, fill="lightgrey", tags="grid")
    for i in range(0, CANVAS_HEIGHT, GRID_SPACING):
        CANVAS.create_line(0, i, CANVAS_WIDTH, i, fill="lightgrey", tags="grid")
    
    # Draw thicker X and Y axes
    CANVAS.create_line(CANVAS_WIDTH / 2, 0, CANVAS_WIDTH / 2, CANVAS_HEIGHT, fill="#3B3B3B", width=2, tags="grid")
    CANVAS.create_line(0, CANVAS_HEIGHT / 2, CANVAS_WIDTH, CANVAS_HEIGHT / 2, fill="#3B3B3B", width=2, tags="grid")


def resize_canvas(event):
    """
    Adjusts the canvas and scaling dynamically when the window is resized to ensure the points stay proportionate no matter the canvas size.
    :param event: Thinker event listener.
    """
    global CANVAS_WIDTH, CANVAS_HEIGHT, SCALE
    CANVAS_WIDTH, CANVAS_HEIGHT = event.width, event.height
    SCALE = min(CANVAS_WIDTH, CANVAS_HEIGHT) / 50  # Keep the grid proportional
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
    # If we have a convex hull, redraw it too
    if CONVEX_HULL_DATA:
        calculate_convex_hull()


# Plot a point on the canvas
def plot_point(point, size=5, label=False, **kwargs):
    """
    Draw a specific point on the canvas at the specified coordinates
    :param point: Point (x, y) coordinate in tuple.
    :param size: Size of the point oval.
    :param label: Whether display coordinate label, default is not.
    :param kwargs: Additional keyword arguments for 'create_oval'.
    :return:
    """
    screen_x, screen_y = math_to_screen(*point)  # Convert math coords to screen coords
    CANVAS.create_oval(screen_x - size, screen_y - size, screen_x + size, screen_y + size, **kwargs)
    if label:
        CANVAS.create_text(screen_x, screen_y + 15, text=f"({point[0]:.1f}, {point[1]:.1f})", fill="#5A5A5A", tags="points")

def draw_polygon(points, color, width=2, tags="polygon"):
    """
    Draws the convex hull by connect a list of points with lines
    :param points: set of points making up the polygon
    :param colour: colour of the polygon
    :param width: the width of the lines to use to create the polygon
    :param tags: used to keep track of the points that make up the polygons
    """
    for i in range(len(points)):
        line_point(points[i], points[(i + 1) % len(points)], fill=color, width=width, tags=tags)

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

def user_plot(event):
    """
    Add a point where the user clicks on the canvas.
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
    Update the display to show how many points are currently on the canvas.
    """
    POINT_COUNT_LABEL.config(text=f"Points: {len(POINTS)}")

def reset_canvas():
    """
    Clears all the points on the canvas and resets it to its inital state
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
    Compute and visualize the convex hull for the current set of points.
    :return: None
    """
    global CONVEX_HULL_DATA
    CANVAS.delete("hull")  # Remove any previous hull
    CONVEX_HULL_DATA = quickhull.quick_hull(POINTS)  # Run the QuickHull algorithm
    hull = CONVEX_HULL_DATA[0]  # Get the list of hull points
    draw_polygon(hull, color="#0078D4", width=2, tags="hull")  # Draw the hull
    for point in hull:  # Highlight each hull point
        plot_point(point, size=7, fill="#00C853", tags="hull")
    BUTTONS["steps-button"].config(state=tk.NORMAL)  # Enable the "steps" button


# --- Additional Functionalities ---

def show_steps():
    """
    Show the iterative steps taken by the QuickHull algorithm to compute the convex hull.
    :return: None
    """
    if CONVEX_HULL_DATA is None:  # Ensure the convex hull has been calculated
        return
    
    steps = CONVEX_HULL_DATA[1]  # Extract the list of intermediate steps
    CANVAS.delete("steps")  # Clear previous step visualizations
    toggle_buttons(state=tk.DISABLED)

    def visualize_step(i):
        """
        Display the convex hull of the specific step.
        :param points: List of points for the step.
        :return: None
        """
        CANVAS.delete("steps") 
        step_points = steps[:i + 1]  # Get the points up to this step
        step_hull = quickhull.quick_hull(step_points)[0]  # Calculate the hull for this step
        draw_polygon(step_hull, color="orange", tags="steps")  
        for point in step_hull: 
            plot_point(point, size=6, fill="lightgreen", tags="steps")

    # Schedule each step to be shown with a delay for visual effect
    for i in range(len(steps)):
        ROOT.after(i * 500, lambda i=i: visualize_step(i))

    # Once all steps have been shown, re-enable the buttons
    ROOT.after(len(steps) * 500, lambda: toggle_buttons(state="normal"))

def peel_layers():
    """
    Iterately calls the quick_hull algorithm and visualises the convex hulls at each layer.
    Each "layer" represents an outer layer of points forming part of the convex hull.
    """
    CANVAS.delete("peel")
    points = POINTS[:]  # Copy the points list so we can modify it
    layer_colors = ["#FFC107", "#4CAF50", "#FF5722", "#03A9F4", "#673AB7"]
    layer_index = 0  # Start from the first color

    if not points:
        return

    while points:  
        hull = quickhull.quick_hull(points)[0]  # Calculate the convex hull for the remaining points
        if not hull:  # If no hull is found, stop
            break
        draw_polygon(hull, color=layer_colors[layer_index % len(layer_colors)], width=2, tags="peel")
        for point in hull:  # Highlight the points that form the hull
            plot_point(point, size=7, fill=layer_colors[layer_index % len(layer_colors)], tags="peel")
        points = [p for p in points if p not in hull]  # Remove the points that are part of this hull
        layer_index += 1  # Move to the next layer color


# Generate random points
def generate_random_points(num_points=20):
    """
    Generate a random set of points on the graph
    :param num_points: The number of points to randomly place on the canvas
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
    """
    Initialize the main Tkinter window and set up the canvas and buttons.
    This is where the visualization and user interaction is set up.
    """
    CANVAS_WIDTH, CANVAS_HEIGHT = 600, 600  
    GRID_SPACING, SCALE = 25, 12.5  
    POINTS = []  # List to store user-selected points
    CONVEX_HULL_DATA = None  # Will hold the data related to the convex hull

    ROOT = tk.Tk()  
    ROOT.title("QuickHull Visualization")
    ROOT.configure(bg="#2E2E2E") 

    style = ttk.Style() 
    style.theme_use("clam")
    style.configure("TButton", padding=4, font=("Arial", 12), foreground="#FFFFFF", background="#80669d")
    style.configure("TLabel", font=("Arial", 12), foreground="#FFFFFF", background="#2E2E2E")

    # Create the main canvas where we will draw the points and hull
    CANVAS = tk.Canvas(ROOT, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#F4F4F4", highlightthickness=0)
    CANVAS.grid(row=0, column=0, columnspan=5, sticky="nsew")  # Position the canvas on the grid
    CANVAS.bind("<Button-1>", user_plot)  # Bind the left mouse click to add points
    CANVAS.bind("<Configure>", resize_canvas)  # Bind window resizing to scale the points and canvas

    # Set up the layout of the window with a grid system
    ROOT.rowconfigure(0, weight=1)
    ROOT.columnconfigure(0, weight=1)

    # Create a label to display the number of points
    POINT_COUNT_LABEL = ttk.Label(ROOT, text="Points: 0")
    POINT_COUNT_LABEL.grid(row=1, column=0, columnspan=5)

    # Define the buttons and their actions
    BUTTONS = {
        "reset-button": ttk.Button(ROOT, text="Reset", command=reset_canvas),
        "calculate-button": ttk.Button(ROOT, text="Calculate Convex Hull", command=calculate_convex_hull),
        "steps-button": ttk.Button(ROOT, text="Show Steps", command=show_steps, state=tk.DISABLED),
        "layers-button": ttk.Button(ROOT, text="Peel Layers", command=peel_layers),
        "random-button": ttk.Button(ROOT, text="Generate Random Points", command=lambda: generate_random_points(random.randint(5,25))),
    }

    # Arrange the buttons in the grid
    for i, button in enumerate(BUTTONS.values()):
        button.grid(row=2, column=i)

    draw_grid()  # Draw the initial grid
    ROOT.mainloop()  # Start the Tkinter event loop
