class Point:
    def __init__(self, name, x, y, parent):
        self.name = name
        self.x, self.y = x, y
        self.parent = parent


class Intersection(Point):
    def __init__(self, name, x, y, parent1, parent2):
        self.name = name
        self.x, self.y = x, y
        self.parent1 = parent1
        self.parent2 = parent2


class Segment:
    def __init__(self, a, b):
        self.point1 = a
        self.point2 = b


class Circle:
    def __init__(self, a, radius):
        self.point = a
        self.radius = radius


class Rectangle:
    def __init__(self, a, b, c, d):
        self.point = a
        self.point2 = b
        self.point3 = c
        self.point4 = d


class Square(Rectangle):
    def __init__(self, a, b, c, d):
        self.point = a
        self.point2 = b
        self.point3 = c
        self.point4 = d


class Scheme:
    points = {}
    intersection = {}
    segments = {}
    circle = {}
    global points, intersection, segments, circle

    def add_point(self, name, x, y, parent):
        global points
        points[name] = [x, y, parent]

    def add_intersection(self, name, x, y, parent):
        global intersection
        intersection[name] = [x, y, parent]

    def add_segments(self, a, b):
        global segments, points
        segments[a, b] = [points[a][0], points[a][1], points[b][0], points[b][1]]

    def add_circle(self, a, radius):
        global circle
        circle[a] = "Radius {}".format(radius)

    def get_points(self, name):
        global points
        return points[name]

    def get_intersection(self, name):
        global intersection
        return intersection[name]

    def get_segment(self, a, b):
        global segments
        return segments[a, b]

    def get_circle(self, a):
        global circle
        return circle[a]
