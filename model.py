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

    def __init__(self):
        self.points = []
        self.intersections = []
        self.segments = []
        self. circles = []

    def add_point(self, name, x, y, parent):
        self.points.append(Point(name, x, y, parent))

    def add_intersection(self, name, x, y, parent1, parent2):
        self.intersection.append(Intersection(name, x, y, parent1, parent2))

    def add_segments(self, a, b):
        self.segments.append((self.points[a][0], self.points[a][1]), (self.points[b][0], self.points[b][1]))

    def add_circle(self, a, radius):
        self.circle.append(Circle(a, radius))

    def get_points(self, name):
        for point in self.points:
            if name == point.name:
                return point

    def get_intersection(self, name):
        for intersection in self.intersections:
            if intersection.name == name:
                return intersection

    def get_segment(self, a, b):
        for segment in self.segments:
            if segment.point1 == a and segment.point2 == b:
                return segment

    def get_circle(self, a):
        for circle in self.circles:
            if circle.point == a:
                return circle
