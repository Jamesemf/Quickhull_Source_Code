"""
QuickHull Algorithm Implementation

Author: James Ford
"""


def cross_product(p1: tuple, p2: tuple, p3: tuple) -> float:
    """
    Compute the cross product of vectors 'p1p2' and 'p1p3' to measure the relative orientation.
    Positive values indicate a left turn, negative values indicate a right turn, and zero indicates collinearity.

    Args:
        p1 (tuple): Coordinates of the first point (x1, y1).
        p2 (tuple): Coordinates of the second point (x2, y2).
        p3 (tuple): Coordinates of the third point (x3, y3).

    Returns:
        float: The cross product value, representing the orientation of p3 relative to the line segment p1-p2.

    """
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def quick_hull(points: list) -> tuple:
    """
    Compute the convex hull of a set of 2D points using the QuickHull algorithm.

    Args:
        points (list): A list of tuples representing 2D points, e.g., [(x1, y1), (x2, y2), ...].

    Returns:
        tuple: A tuple containing:
            - A list of convex hull points in counter-clockwise order.
            - A list of points in the order they were added to the convex hull

    """
    # Used to keep track of the order points are found
    search_order = []

    # Remove duplicate points but preserve order
    points = list(dict.fromkeys(points))

    # Validate input
    if not all(isinstance(point, tuple) and len(point) == 2 for point in points):
        raise ValueError("Input points must be a list of 2D coordinate tuples.")
    
    # Identify the leftmost and rightmost points
    p1 = min(points, key=lambda p: p[0])  # Leftmost
    p2 = max(points, key=lambda p: p[0])  # Rightmost
    search_order.append(p1)
    search_order.append(p2)

    # Split points into upper and lower subsets based on their orientation relative to the line p1-p2
    upper_hull = []
    lower_hull = []
    for p in points:
        cross_product_value = cross_product(p1, p2, p)
        # '0' Cross product value indicate the point is on line 'ab' and should be ignored.
        if cross_product_value > 0:
            upper_hull.append(p)
        if cross_product_value < 0:
            lower_hull.append(p)

    # Recursively find hull points for each subset
    above_hull = find_hull(search_order, upper_hull, p1, p2)
    above_hull.append(p2)
    below_hull = find_hull(search_order, lower_hull, p2, p1)
    below_hull.append(p1)

    # Combine hull points
    convex_hull = above_hull + below_hull
    return convex_hull, search_order

def find_hull(search_order: list, point_set: list, p1: tuple, p2: tuple) -> list:
    """
    Recursively calculate convex hull points within a subset.

    This function identifies the furthest point from the line segment p1-p2, divides the subset into two regions 
    based on the point, and processes each region recursively to identify all convex hull points.

    Args:
        search_order (list): List to track the order in which points are added to the convex hull.
        point_set (list): Subset of points to process.
        p1 (tuple): Starting point of the line segment.
        p2 (tuple): Ending point of the line segment.

    Returns:
        list: A subset of convex hull points.

    """
    if not point_set:
        return []
    
    # Find the furthest point from the line p1-p2
    furthest = max(point_set, key=lambda p: abs(cross_product(p1, p2, p)))
    
    # Add the furthest point to the search order
    search_order.append(furthest)

    # Divide points into subsets based on their position relative to the lines p1-furthest and furthest-p2
    left_set = [p for p in point_set if cross_product(furthest, p, p1) > 0]
    right_set = [p for p in point_set if cross_product(p2, p, furthest) > 0]

    # Recursive calls to find hull points
    left_hull = find_hull(search_order, left_set, p1, furthest)
    right_hull = find_hull(search_order, right_set, furthest, p2)
    
    # Append the furthest point to the hull
    left_hull.append(furthest)
    
    # Return points found in recursion
    return left_hull + right_hull


if __name__ == '__main__':
    print("\n[QuickHull Algorithm]\nThis script computes the convex hull of a set of 2D points.")
    print("To test with a GUI, execute 'visualise.py'")
    print("Reference Readme for more details")
