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
        self.error = 10

    def add_point(self, x: float, y: float):
        name = self.generate_name(Point)
        self.translator.connector.assert_code(f'point({name})')
        self.points[name] = Point(x, y, name)

    def add_segment(self, a: Point, b: Point):
        name = self.generate_name(Segment)
        new_segment = Segment(a, b)
        for segment in self.segments:
            if segment == new_segment:
                self.translator.connector.assert_code(f'congruent(segment({segment.point1.name},'
                                                      f' {segment.point2.name}),'
                                                      f' segment({new_segment.point1.name},'
                                                      f' {new_segment.point2.name}))')
        self.segments[name] = new_segment

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

    @staticmethod
    def correcting_points_warning(point, segments, circles):
        error = 4
        for _, i in circles.items():
            print(str(i))
            list = i.intersectionLine(Line(i.center, point))
            if not list:
                return point
            for j in list:
                condition = -error <= point - j <= error
                print(str(j), str(point))
                if condition:
                    point.x = j.x
                    point.y = j.y
        return point

    def correcting_online_points(self, point: Point) -> Point:
        for segment in self.segments.values():
            if segment.pointBelongs(Point, self.error):
                pass
                # return point + point.asd(segment)
