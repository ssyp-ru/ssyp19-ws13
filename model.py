from Translator import Translator
from geom import *
from string import ascii_uppercase as dictionary

# Review: I thought you like type hints.

class Model:

    def __init__(self):
        self.points = {}
        self.segments = {}
        self.circles = {}
        self.operations = []
        self.error = 4

    def add_point(self, x: float, y: float):
        self.points[self.generate_name(Point)] = Point(x, y)

    def add_segment(self, a: Point, b: Point):
        self.segments[self.generate_name(Segment)] = Segment(a, b)

    def add_circle(self, a: Point, radius: float):
        self.circles[self.generate_name(Circle)] = Circle(a, radius)

    def generate_name(self, type: type) -> str:
        if type is Circle:
            return self.generate_name_by_number(len(self.circles))
        elif type is Segment:
            return self.generate_name_by_number(len(self.segments))
        elif type is Point:
            return self.generate_name_by_number(len(self.points))

    @staticmethod
    # Review: Why should it be static?
    def generate_name_by_number(num: int) -> str:
        if num <= 25:
            return dictionary[num]
        else:
            firstletter = dictionary[(num // 26)]
            secondletter = dictionary[(num % 26)]
            return firstletter + secondletter

    def correcting_points(self, start: Point, end: Point) -> Point and Point:
        if self.points:
            for i in self.points.values():
                # Review: Long lines still suck.
                if -self.error <= start - i <= self.error:
                    start = i
                if -self.error <= end - i <= self.error:
                    end = i
            return start, end

    def correcting_online_points(self, point: Point) -> Point:
        for segment in self.segments.values():
            if segment.isPointBelongs(Point, self.error):
                return point + point.asd(segment)