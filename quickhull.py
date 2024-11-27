"""
Quickhull Algorithm Implementation

@author: James Ford
"""


def Find_distance(point_a: tuple, point_b: tuple, point_c: tuple):
    """
    Calculate cross product of vectors 'ca' x 'cb' with formula A x B = Ax * By - Ay * Bx.
    :param point_a: Coordinate of point 'a' in tuple.
    :param point_b: Coordinate of point 'b' in tuple.
    :param point_c: Coordinate of point 'c' in tuple.
    :return: Value of cross product of 'ca' x 'cb'.
    """
    return (point_c[0] - point_a[0]) * (point_c[1] - point_b[1]) - (point_c[1] - point_a[1]) * (point_c[0] - point_b[0])


def subset_hull(search_order: list, point_set: list, point_a: tuple, point_b: tuple):
    """
    Recursively calculate convex hull points in a subset with lining order.
    :param search_order: List for inference order of convex hull points.
    :param point_set: Subset list of points to be calculated.
    :param point_a: Point A tuple for the line.
    :param point_b: Point B tuple for the line.
    :return: Subset list of convex hull points.

    """
    # If there are no more subset, break the recursion.
    if not point_set:
        return []
    # Find the furthest point 'c' to line 'ab' by compare absolute cross product value 'ac' x 'ab'.
    max_value = -1
    furthest = None
    for point in point_set:
        value = abs(Find_distance(point, point_b, point_a))
        if value > max_value:
            furthest = point
            max_value = value
    # Use the point create two edge with the 'ab' line to calculate the two outside
    # subset of each edge for recursion, then concat two results list with the calculated furthest point in middle.
    search_order.append(furthest)
    left_set = [point for point in point_set if Find_distance(furthest, point, point_a) > 0]
    right_set = [point for point in point_set if Find_distance(point_b, point, furthest) > 0]
    
    left_hull = subset_hull(search_order, left_set, point_a, furthest)
    right_hull = subset_hull(search_order, right_set, furthest, point_b)
    left_hull.append(furthest)
    return left_hull + right_hull


def quick_hull(points: list):
    """
    Calculate convex hull from list of points with quick hull method, output two lists of line-up order and inference
    search order.
    :param points: List of points in tuple to be calculated.
    :return: (List of points for convex hull, List of points of inference search order)
    """
    search_order = []
    convex_hull = []

    if not len(points) < 2:
        # Find the left and right most points 'a' and 'b' then add to convex hull.
        # If multiple most points have same x coordinate then find the most y.
        point_a = min(points, key=lambda x: (x[0], x[1]))
        point_b = max(points, key=lambda x: (x[0], x[1]))
        search_order.append(point_a)
        search_order.append(point_b)

        # Seperated remain points which divide by line 'ab' into two sets. Sign of the cross product of the vector
        # 'ab' x 'ac' determine whether the point is located above or below the line segment.
        upper_hull = []
        lower_hull = []
        for point in points:
            cross_product_value = Find_distance(point_b, point, point_a)
            # '0' Cross product value indicate the point is on line 'ab' and should be ignored.
            if cross_product_value > 0:
                upper_hull.append(point)
            if cross_product_value < 0:
                lower_hull.append(point)

        # Add two initial point into each sub-hull to form a complete cycled graph with line-up order.
        above_hull = subset_hull(search_order, upper_hull, point_a, point_b)
        above_hull.append(point_b)
        below_hull = subset_hull(search_order, lower_hull, point_b, point_a)
        below_hull.append(point_a)
        convex_hull = above_hull + below_hull
    return convex_hull, search_order


if __name__ == '__main__':
    print("\n[QuickHull Algorithm] This is the algorithm for QuickHull, for GUI test please execute \"thinker.py\"!\n")

