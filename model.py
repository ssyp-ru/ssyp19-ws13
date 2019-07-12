from Translator import Translator
from geom import *
from string import ascii_lowercase as dictionary
from scipy.optimize import fsolve

class Model:

    def __init__(self):
        self.translator = Translator()
        self.points = {}
        self.segments = {}
        self.circles = {}
        self.operations = []
        self.alloperations = []
        self.CongruentSegments = {}
        self.error = 6

    def add_point(self, x: float, y: float, Fixed = False, parent1 = None, parent2 = None):
        name = self.generate_name()
        point = Point(x, y, name)
        if not Fixed:
            # print(str(point))
            self.points[name] = point
            self.translator.connector.prolog.assertz(f'point({name})')
        elif isinstance(parent2, Circle) and isinstance(parent1, Segment):
            points = parent2.intersectionSegment(parent1)
            if len(points) > 1:
                for i, el in enumerate(points):
                    if isinstance(self.pointExist(el), Point):
                        point = DependPoint(name, parent1, parent2, i)
                        self.points[name] = point
                        name = self.generate_name()
                        self.translator.connector.prolog.assertz(f'point({name})')
                return point
            else:
                point = DependPoint(name, parent1, parent2)
                if isinstance(self.pointExist(point), Point):
                    self.points[name] = point
                    name = self.generate_name()
                    self.translator.connector.prolog.assertz(f'point({name})')
        else:
            point = DependPoint(name, parent1, parent2)
            self.points[name] = point
            self.translator.connector.prolog.assertz(f'point({name})')
        for segment in self.segments.values():
            if segment.pointBelongs(point):
                self.translator.connector.prolog.assertz(\
                    f'laysBetween({segment.point1.name}, {segment.point2.name}, {point.name})')
                #print(self.translator.connector.get_n_ans_new(\
                #    f'isCongruent({segment.point1.name}, {segment.point2.name})'))
        return point 

    def add_segment(self, a: Point, b: Point):
        new_segment = Segment(a, b)
        split = {}
        for k, segment in self.segments.items():
            interpoint = new_segment.intersection(segment)
            if interpoint:
                if isinstance(self.pointExist(interpoint), Point):
                    n_point = self.add_point(1, 1, True, new_segment, segment)
                    split[k] = (n_point, new_segment.point1, new_segment.point2, segment.point1, segment.point2)
                    # TODO: if error - commend from here
                    break
        if split:
            del self.segments[k]
        for k, v in split.items():
            for point in v[1::]:
                self.add_segment(v[0], point)
        if split:
            return None
        # to here
        for circle in self.circles.values():
            interpoint = circle.intersectionSegment(Segment(new_segment.point1, new_segment.point2))
            if interpoint:
                self.add_point(1, 1, True, new_segment, circle)

        for segment in self.segments.values():
            if -error - 10 < segment.length - new_segment.length < error + 10:
                segment1 = f'segment({segment.point1.name}, {segment.point2.name})'
                segment2 = f'segment({new_segment.point1.name}, {new_segment.point2.name})'
                self.translator.connector.prolog.assertz(f'congruent({segment1}, {segment2})')
        self.segments[a.name + b.name] = new_segment
        return new_segment

    def add_circle(self, segment: Segment):
        circle = Circle(segment)
        self.circles[segment.point1.name+segment.point2.name] = circle
        return circle

    def generate_name(self, index=None) -> str:
        if not index:
            num = len(self.points)
        else:
            num = index
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
            if abs(abs(radial)-circle.radius) < error:
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
        self.translator.connector.retract_code('point(X);segment(A, B);laysBetween(A, B, C);congruent(A,B)', all=True)

    def pointExist(self, point):
        for _, i in self.points.items():
            if point == i:
                return True
        return point

    def correctingScheme(self):
        def equation(inputvector):
            tempmodel = self.copy()
            i = 0
            for point in tempmodel.points.values():
                if not isinstance(point, DependPoint):
                    point.x = inputvector[i]
                    point.y = inputvector[i + 1]
                    i += 2
            y = [0] * len(inputvector)
            X = []
            j = 0
            while X:
                X = tempmodel.getCongruencyClass(j)
                avglen = sum([el.length for el in X]) / len(X)
                print(sum([abs(el.length - avglen) for el in X]))
                y[j] = sum([abs(el.length - avglen) for el in X])
                j += 1
            return y
        inputvector = []
        pointlist = list(self.points.values())
        for i in pointlist:
            inputvector.append(i.x)
            inputvector.append(i.y)
        print(inputvector)
        awnser, data, ok, msg = fsolve(equation, inputvector, full_output=True)
        if ok == 1:
            j = 0
            self.points = {}
            print(awnser)
            for i in range(int(len(awnser) / 2)):
                self.add_point(awnser[2 * j], awnser[(2 * j) + 1])
                j += 1
    
    def findPointFromName(self, name):
        res = self.points.get(str(name))
        return res

    def getCongruencyClass(self, index):
        i = 0
        if not index > len(self.CongruentSegments):
            for key, val in self.CongruentSegments.items():
                if i == index:
                    val.add(key)
                    return val
                i += 1
        return
    def copy(self):
        model = Model()
        model.points = self.points.copy()
        model.CongruentSegments = self.CongruentSegments.copy()
        return model