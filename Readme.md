# QuickHull Algorithm

This project implements the **QuickHull Algorithm** for computing the convex hull of a set of 2D points.
## Features

- Efficiently computes the convex hull of a set of points.
- Handles duplicate points by removing them.
- Returns the points of the convex hull in counter-clockwise order.
- Validates input for correct format and dimensions.

---

## How It Works

The QuickHull algorithm works by:

1. Identifying the leftmost and rightmost points as the initial line segment of the convex hull.
2. Dividing the remaining points into two subsets based on their position relative to this line.
3. Recursively finding the furthest point from the current line segment and updating the convex hull.
4. Combining the results of the upper and lower hulls to form the final convex hull.

The algorithm relies on the **cross product** to determine the orientation of points relative to a line.

---

## Getting Started

### Prerequisites

- Python 3.6 or newer.
- tkinter

### Usage

1. Clone or download this repository.
2. Run the `visualise.py` script:   "python visualise.py" (quickhull.py must be in the same directory)