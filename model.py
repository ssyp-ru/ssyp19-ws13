from Translator import Translator
from geom import *


class Model:

    def __init__(self):
        self.points = {}
        self.segments = {}
        self.circles = {}
        self.operations = []

    def add_point(self, x, y):
        self.points[self.generate_name(Point)] = Point(x, y)

    def add_segment(self, a, b):  # FIXME: watch this if strange results!
        self.segments[self.generate_name(Segment)] = Segment(a, b)

    def add_circle(self, a, radius):
        self.circles[self.generate_name(Circle)] = Circle(a, radius)

    def generate_name(self, type):
        if type is Circle:
            return self.generate_name_by_number(len(self.circles))
        elif type is Segment:
            return self.generate_name_by_number(len(self.segments))
        elif type is Point:
            return self.generate_name_by_number(len(self.points))

    @staticmethod
    def generate_name_by_number(num):
        dictionary = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                      "T", "U", "V", "W", "X", "Y", "Z"]
        if num <= 25:
            return dictionary[num]
        else:
            firstletter = dictionary[(num // 26)]
            secondletter = dictionary[(num % 26)]
            return firstletter + secondletter
