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

    def add_point(self, x: float, y: float):
        self.points[self.generate_name(Point)] = Point(x, y)

    def add_segment(self, a: Point, b: Point):
        self.segments[self.generate_name(Segment)] = Segment(a, b)

    def add_circle(self, a: Point, radius: float):
        self.circles[self.generate_name(Circle)] = Circle(a, radius)

    def generate_name(self, type: type):
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
