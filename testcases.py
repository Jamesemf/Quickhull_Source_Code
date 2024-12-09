import unittest
from quickhull import quick_hull

class TestQuickHull(unittest.TestCase):
    def test_simple_square(self):
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        expected_hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
        convex_hull, search_order = quick_hull(points)
        self.assertCountEqual(convex_hull, expected_hull)

    def test_collinear_points(self):
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        expected_hull = [(0, 0), (3, 3)]
        convex_hull, search_order = quick_hull(points)
        self.assertCountEqual(convex_hull, expected_hull)

    def test_triangle(self):
        points = [(0, 0), (4, 0), (2, 3), (2, 1)]
        expected_hull = [(0, 0), (4, 0), (2, 3)]
        convex_hull, search_order = quick_hull(points)
        self.assertCountEqual(convex_hull, expected_hull)

    def test_duplicate_points(self):
        points = [(0, 0), (4, 0), (2, 3), (2, 1), (0, 0), (4, 0)]
        expected_hull = [(0, 0), (4, 0), (2, 3)]
        convex_hull, search_order = quick_hull(points)
        self.assertCountEqual(convex_hull, expected_hull)

    def test_complex_shape(self):
        points = [
            (0, 0), (4, 0), (2, 3), (6, 2), (5, 5), (3, 4),
            (2, 2), (1, 4), (4, 6), (0, 5), (6, 5)
        ]
        expected_hull = [(0, 0), (4, 0), (6, 2), (6, 5), (4, 6), (0, 5)]
        convex_hull, search_order = quick_hull(points)
        self.assertCountEqual(convex_hull, expected_hull)

    def test_single_point(self):
        points = [(1, 1)]
        expected_hull = [(1, 1)]
        convex_hull, search_order = quick_hull(points)
        print(convex_hull)
        print(expected_hull)
        self.assertCountEqual(convex_hull, expected_hull)

    def test_two_points(self):
        points = [(1, 1), (2, 2)]
        expected_hull = [(1, 1), (2, 2)]
        convex_hull, search_order = quick_hull(points)
        self.assertCountEqual(convex_hull, expected_hull)

    def test_empty_set(self):
        points = []
        expected_hull = []
        convex_hull, search_order = quick_hull(points)
        self.assertCountEqual(convex_hull, expected_hull)


if __name__ == '__main__':
    unittest.main()