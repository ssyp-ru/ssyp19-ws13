from Translator import Translator
from geom import *
from string import ascii_lowercase as dictionary


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
        self.translator.connector.prolog.assertz(f'point({name})')
        self.points[name] = p
        for segment in self.segments.values():
            if segment.pointBelongs(p):
                self.translator.connector.prolog.assertz(\
                    f'laysBetween({segment.point1.name}, {segment.point2.name}, {name})')
                print(self.translator.connector.get_n_ans_new(\
                    f'isCongruent({segment.point1.name}, {segment.point2.name})'))
        return p

    def add_segment(self, a: Point, b: Point):
        new_segment = Segment(a, b)
        for segment in self.segments.values():
            if -1 < segment.length - new_segment.length < 1:
                segment1 = f'segment({segment.point1.name}, {segment.point2.name})'
                segment2 = f'segment({new_segment.point1.name}, {new_segment.point2.name})'
                self.translator.connector.prolog.assertz(f'congruent({segment1}, {segment2})')
        self.segments[a.name + b.name] = new_segment
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

    def correctingPoints(self, point, segments, circles):
        error = 8

        for circle in circles.values():
            radial = point-circle.center
            if (abs(radial)-circle.radius) < error:
                unit = radial/abs(radial)
                point = circle.center + unit*circle.radius
                point.parent1 = circle
            return point
        for i in segments.values():
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
        del self.translator
        self.translator = Translator()
