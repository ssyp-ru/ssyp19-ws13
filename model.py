from Translator import Translator
from geom import *
from string import ascii_uppercase as dictionary


class Model:

    def __init__(self):
        self.translator = Translator()
        self.points = {}
        self.segments = {}
        self.circles = {}
        self.operations = []
        self.alloperations = []
        self.error = 8

    def add_point(self, x: float, y: float):
        name = self.generate_name()
        p = Point(x, y, name)
        self.points[name] = p
        return p

    def add_segment(self, a: Point, b: Point):
        new_segment = Segment(a, b)
        self.segments[a.name+b.name] = new_segment
        return new_segment

    def add_circle(self, segment: Segment):
        circle = Circle(segment)
        self.circles[segment.point1.name+segment.point2.name] = circle
        return circle

    def generate_name(self) -> str:
        num = len(self.points)
        if num <= 25:
            return dictionary[num]
        else:
            firstletter = dictionary[(num // 26) - 1]
            secondletter = dictionary[(num % 26)]
            return firstletter + secondletter

    def correcting_points(self, start: Point, end: Point) -> Point and Point:
        if self.points:
            for i in self.points.values():
                if -self.error <= start - i <= self.error:
                    start = i
                if -self.error <= end - i <= self.error:
                    end = i
        return start, end

    def correctingPoints(point, segments, circles):
        error = 8
        for _, i in circles.items():
            list = i.intersectionLine(geometry.Line(i.center, point))
            if not list:
                return point
            for j in list:
                condition = -error <= point - j <= error
                if condition:
                    point.x = j.x
                    point.y = j.y
        for _, i in segments.items():
            if point.distToSegment(i) < error:
                return point.projectionOnSegment(i)
        return point

    def check_segment(self, point1, point2):
        names = (point1.name + point2.name, point2.name + point1.name)
        for name in names:
            if name in self.segments.keys():
                return self.segments[name]
        return self.add_segment(point1, point2)

    def check_circle(self, segment, error=10):
        for circle in self.circles.values():
            if circle.center == segment.point1 and abs(circle.radius - segment.length) <= error:
                return circle
        return self.add_circle(segment)

    def reset_prolog(self):
        self.translator = Translator()