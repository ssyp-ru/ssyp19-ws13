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
        name = self.generate_name(Point)
        self.translator.connector.assert_code(f'point({name})')
        p = Point(x, y, name)
        self.points[name] = p
        return p

    def add_segment(self, a: Point, b: Point):
        new_segment = Segment(a, b)
        for segment in self.segments.values():
            if segment.length == new_segment.length:
                self.translator.connector.assert_code(f'congruent(segment({segment.point1.name},'
                                                      f' {segment.point2.name}),'
                                                      f' segment({new_segment.point1.name},'
                                                      f' {new_segment.point2.name}))')
        self.segments[self.generate_name(Segment)] = new_segment
        return new_segment

    def add_circle(self, segment: Segment):
        circle = Circle(segment)
        self.circles[self.generate_name(Circle)] = circle
        return circle

    def generate_name(self, type: int) -> str:
        if type is Circle:
            num = len(self.circles)
        elif type is Segment:
            num = len(self.segments)
        elif type is Point:
            num = len(self.points)
        else:
            num = type
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
