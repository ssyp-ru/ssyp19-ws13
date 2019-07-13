from Translator import Translator
from geom import *
from string import ascii_lowercase as dictionary
from scipy.optimize import fsolve
from itertools import cycle

class Model:

    def __init__(self):
        self.translator = Translator()
        self.points = {}
        self.segments = {}
        self.circles = {}
        self.operations = []
        self.alloperations = []
        self.CongruentSegments = {}
        self.dependpoints = {}
        self.error = 6

    def add_point(self, x: float, y: float, Fixed = False, parent1 = None, parent2 = None):
        name = self.generate_name()
        point = Point(x, y, name)
        if not Fixed:
            self.points[name] = point
            self.translator.connector.prolog.assertz(f'point({name})')
        elif isinstance(parent2, Circle) and isinstance(parent1, Segment):
            points = parent2.intersectionSegment(parent1)
            if len(points) > 1:
                for i, el in enumerate(points):
                    for existing in self.points.values():
                        if el.distToPoint(existing) < error:
                            return existing
                    else:
                        point = DependPoint(name, parent1, parent2, i)
                        self.dependpoints[name] = point
                        name = self.generate_name()
                        self.translator.connector.prolog.assertz(f'point({name})')
                return point
            else:
                point = DependPoint(name, parent1, parent2)
                if isinstance(self.pointExist(point), Point):
                    self.dependpoints[name] = point
                    name = self.generate_name()
                    self.translator.connector.prolog.assertz(f'point({name})')
        else:
            point = DependPoint(name, parent1, parent2)
            self.dependpoints[name] = point
            self.translator.connector.prolog.assertz(f'point({name})')
        for segment in self.segments.values():
            if segment.pointBelongs(point):
                self.translator.connector.prolog.assertz(\
                    f'laysBetween({segment.point1.name}, {segment.point2.name}, {point.name})')
        return point 

    def add_segment(self, a: Point, b: Point):
        if a.name > b.name:
            a, b  = b, a
        new_segment = Segment(a, b)
        split = {}
        for k, segment in self.segments.items():
            interpoint = new_segment.intersection(segment)
            if interpoint:
                if isinstance(self.pointExist(interpoint), Point):
                    self.add_point(1, 1, True, segment, new_segment)
        for circle in self.circles.values():
            interpoint = circle.intersectionSegment(Segment(new_segment.point1, new_segment.point2))
            if interpoint:
                self.add_point(1, 1, True, new_segment, circle)
        self.segments[a.name + b.name] = new_segment
        return new_segment

    def add_circle(self, segment: Segment):
        circle = Circle(segment)
        self.circles[segment.point1.name+segment.point2.name] = circle
        return circle

    def generate_name(self, index=None) -> str:
        if not index:
            num = len(self.points) + len(self.dependpoints)
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
        if point in self.points.values():
            return True
        return point

    def updateCongruencyClasses(self):
        """
            UNUSED. (I hope.)
        """
        solutions = self.translator.connector.get_n_ans_new("congruented(X, Y)")[0]
        for el in solutions:
            point1 = self.findPointFromName(el['X'].args[0])
            point2 = self.findPointFromName(el['X'].args[1])
            point3 = self.findPointFromName(el['Y'].args[0])
            point4 = self.findPointFromName(el['Y'].args[1])
            Xsegment = Segment(point1, point2)
            Ysegment = Segment(point3, point4)
            if Xsegment not in self.CongruentSegments:
                self.CongruentSegments[Xsegment] = set()
            self.CongruentSegments[Xsegment].add(Ysegment)

    def updateEverything(self):
        toUpdate = []
        for segment in self.segments.values():
            if not isinstance(segment.point1, DependPoint) or\
               not isinstance(segment.point2, DependPoint):
                   toUpdate.append(segment)

    def correctingScheme(self):
        def modelToVector():
            vector = []
            for point in sorted(self.points):
                vector.append(self.points[point].x)
                vector.append(self.points[point].y)
            return vector
        def vectorToModel(vector):
            index = 0
            for point in sorted(self.points):
                self.points[point].x, self.points[point].y = vector[index:index+2]
                index += 2
            self.updateEverything()
        def makeConstraints():
            solutions = self.translator.connector.get_n_ans_new("congruented(X, Y)")[0]
            result = {}
            for sol in solutions:
                a,b = sol['X'].args
                c,d = sol['Y'].args
                point1 = self.findPointFromName(a)
                point2 = self.findPointFromName(b)
                point3 = self.findPointFromName(c)
                point4 = self.findPointFromName(d)
                result[point1, point2] = point3, point4
            return result        
        constraints = makeConstraints() 
        def equation(inputvector):
            N = len(inputvector)
            vectorToModel(inputvector)
            y = [0] * len(inputvector)
            for j, cons in zip(range(N), cycle(constraints.items())):
                ab, cd = cons
                a, b = ab
                c, d = cd
                y[j] = abs(abs(a-b)-abs(c-d))
            return y
        initial = modelToVector()

        answer, data, ok, msg = fsolve(equation, initial, full_output=True)
        if not ok:
            vectorToModel(initial)
            return
        vectorToModel(answer)
        self.updateEverything()

    
    def findPointFromName(self, name):
        res = self.points.get(str(name))
        return res

    def copy(self):
        model = Model()
        model.points = self.points.copy()
        model.CongruentSegments = self.CongruentSegments.copy()
        return model

