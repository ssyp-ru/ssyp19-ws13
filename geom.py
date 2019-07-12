import math
# from Translator import Translator
# translator = Translator()


class LineError(ValueError):
    pass


class Circle:

    def intersectionLine(self, line):
        C = line.C + (line.A * self.center.x) + (line.B * self.center.y)
        Acoefficient = line.B * line.B + line.A * line.A
        Bcoefficient = 2 * line.A * C
        Ccoefficient = C * C - line.B * line.B * self.radius * self.radius
        Discriminant = Bcoefficient * Bcoefficient - (4 * Acoefficient * Ccoefficient)
        if Discriminant < 0:
            return
        x1 = (-Bcoefficient + math.sqrt(Discriminant)) / (2 * Acoefficient)
        x2 = (-Bcoefficient - math.sqrt(Discriminant)) / (2 * Acoefficient)
        y1 = (-C - x1 * line.A) / line.B
        y2 = (-C - x2 * line.A) / line.B

        return [Point(x1 + self.center.x, y1 + self.center.y),
                Point(x2 + self.center.x, y2 + self.center.y)]

    def intersectionSegment(self, segment):
        segmentLine = Line(segment.point1, segment.point2)
        interpoints = self.intersectionLine(segmentLine)
        if not interpoints:
            return
        return [i for i in interpoints if segment.pointBelongs(i)]

    def intersectionCircle(self, circle):
        RadiusSqw1 = self.radius * self.radius
        RadiusSqw2 = circle.radius * circle.radius
        Xshifted = circle.center.x - self.center.x
        Yshifted = circle.center.y - self.center.y
        XshiftedSqw = Xshifted * Xshifted
        YshiftedSqw = Yshifted * Yshifted
        AnewLine = 2 * Xshifted
        BnewLine = 2 * Yshifted
        CnewLine = RadiusSqw2 - RadiusSqw1 - (XshiftedSqw + YshiftedSqw)
        line = Line(AnewLine, BnewLine, CnewLine)
        line.normalize()
        print(str(line))
        return self.intersectionLine(Line(AnewLine, BnewLine, CnewLine))

    def __init__(self, *args):
        if isinstance(args[0], Segment):
            segment = args[0]
            self.center = segment.point1
            self.radius = segment.length
            self.point = segment.point2
        else:
            if isinstance(args[0], Point):
                a, b, c, *_ = args
            Bshifted = b - a
            Cshifted = c - a
            BshiftedSqwX = Bshifted.x * Bshifted.x
            BshiftedSqwY = Bshifted.y * Bshifted.y
            CshiftedSqwX = Cshifted.x * Cshifted.x
            CshiftedSqwY = Cshifted.y * Cshifted.y
            Denom = 2 * Bshifted.crossProduct(Cshifted)
            FHalfNumerator = (BshiftedSqwX + BshiftedSqwY) * Cshifted.y
            SHalfNumerator = (CshiftedSqwX + CshiftedSqwY) * Bshifted.y
            DesiredX = a.x + (FHalfNumerator - SHalfNumerator) / Denom
            FHalfNumerator = Bshifted.x * (BshiftedSqwX + BshiftedSqwY)
            SHalfNumerator = Cshifted.x * (CshiftedSqwX + CshiftedSqwY)
            DesiredY = a.y + (FHalfNumerator - SHalfNumerator) / Denom
            self.center = Point(DesiredX, DesiredY)
            self.radius = self.center.distToPoint(a)
            self.point = a

    def __str__(self):
        return f"A circle centered at ({str(self.center)}) with radius {self.radius}"
        # I don't know how to do this less


class Segment():
    def pointBelongs(self, point):
        summ = point.distToPoint(self.point1) + point.distToPoint(self.point2)
        return summ <= self.point1.distToPoint(self.point2) + 1

    def intersection(self, segment):
        Mline = Line(self.point1, self.point2)
        interpoint = Mline.intersection(Line(segment.point1, segment.point2))
        if interpoint:
            Fcondition = self.pointBelongs(interpoint)
            Scondition = segment.pointBelongs(interpoint)
            if Fcondition and Scondition:
                return interpoint
        else:
            return

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = point1.distToPoint(point2)

    def __eq__(self, other, error=5):
        return abs(other.length - self.length) <= error

    def __str__(self):
        return f"({str(self.point1)}; {str(self.point2)})"


class Line():
    error = 1.0

    def normalize(self):
        Nvector = Vector(self.A, self.B).unitDirectedVector()
        self.A = Nvector.x
        self.B = Nvector.y
        self.C = -Nvector.dotproduct(self.point1)

    def pointBelongs(self, point):
        ABvector = Vector(self.point2.x - self.point1.x,
                          self.point2.y - self.point1.y)
        ACvector = Vector(point.x - self.point1.y,
                          point.y - self.point1.y)
        return ABvector.crossProduct(ACvector) < self.error

    def intersectionSegment(self, segment):
        interpoint = self.intersection(Line(segment.point1, segment.point2))
        if interpoint:
            if segment.pointBelongs(interpoint):
                return interpoint
        return

    def intersection(self, line):
        Avector = Vector(self.A, self.B)
        denom = Avector.crossProduct(Vector(line.A, line.B))
        if not denom == 0:
            Fnumerator = ((self.B * line.C) - (self.C * line.B))
            Snumerator = (line.A * self.C) - (line.C * self.A)
            return Point(Fnumerator / denom, Snumerator / denom)

    def __init__(self, *args):
        if isinstance(args[0], Point):
            point1, point2 = args
            if ((point1.x == point2.x) and (point1.y == point2.y)):
                raise(LineError("That points are the same"))
            self.point1 = point1
            self.point2 = point2
            self.A = point2.y - point1.y
            self.B = -(point2.x - point1.x)
            Nvector = Vector(self.A, self.B)
            self.C = Nvector.dotproduct(point1)
            self.normalize()
        else:
            self.A, self.B, self.C, *_ = args
            self.normalize()

    def __str__(self):
        return "%0.4f x + %0.4f y + %0.4f = 0" % (self.A, self.B, self.C)


class Vector:
    def dotproduct(self, vector):
        return (self.x * vector.x) + (self.y * vector.y)

    def angle(self, vector):
        multiplied = self.dotproduct(vector)
        lengthsqw = self.length * vector.length
        return math.degrees(math.acos(multiplied / lengthsqw))

    def projection(self, vector):
        Nvector = self.singleDirectedVector()
        return Nvector * (Nvector.dotproduct(vector))

    def unitDirectedVector(self):
        return Vector((self.x / self.length), (self.y / self.length))

    def crossProduct(self, vector):
        return (self.x * vector.y) - (vector.x * self.y)

    def length(self, point):
        return point.distToPoint(Point(0, 0))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = math.hypot(x, y)

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return Vector(self.x / float, self.y / float)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        elif isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other, self.y - other)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __le__(self, other):
        if isinstance(other, Point) or isinstance(other, Vector):
            return self.x <= other.x and self.y <= other.y
        else:
            return self.x <= other and self.y <= other

    def __ge__(self, other):
        if isinstance(other, Point) or isinstance(other, Vector):
            return self.x >= other.x and self.y >= other.y
        else:
            return self.x >= other and self.y >= other

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other, self.y + other)


class Point(Vector):
    def __init__(self, x, y, name=None):
        super().__init__(x, y)
        self.name = name

    def isInCircle(self, circleslist):
        for _, i in circleslist.items():
            if (self.distToPoint(i.center) < i.radius):
                pass
                # translator.connector.call(...)
                # Here i need Vsevolod's code for request in prolog

    def projectionOnLine(self, line):
        PminusQ = line.point1 - line.point2  # Shifting coordinate system to
        OminusQ = self - line.point2  # line.point2
        dotProduct = PminusQ.dotproduct(OminusQ)
        lengthSqw = PminusQ.length * PminusQ.length
        desiredVector = ((PminusQ / lengthSqw) * dotProduct)
        desiredPoint = Point(desiredVector.x, desiredVector.y)
        return line.point2 + desiredPoint

    def projectionOnSegment(self, segment):
        segmentLine = Line(segment.point1, segment.point2)
        projectPoint = self.projectionOnLine(segmentLine)
        if segment.pointBelongs(projectPoint):
            return projectPoint
        return

    def distToPoint(self, point):
        return (self - point).length

    def distToLine(self, line):
        inclined = Vector(line.point1.x - self.x, line.point1.y - self.y)
        cross = inclined.crossProduct(line.point2 - line.point1)
        return abs(cross / (line.point2 - line.point1).length)

    def distToSegment(self, segment):
        inclined = Vector(self.x - segment.point1.x, self.y - segment.point1.y)
        if (inclined.dotproduct(segment.point2 - segment.point1)) < 0:
            return (min(self.distToPoint(segment.point1),
                    self.distToPoint(segment.point2)))
        else:
            return self.distToLine(segment)

    def __add__(self, other):
        if isinstance(other, Point) or isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other, self.y + other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    # redefined sub func
    def __sub__(self, other):
        if isinstance(other, Point) or isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other, self.y - other)

    def __le__(self, other):
        if isinstance(other, Point):
            return self.x <= other.x and self.y <= other.y
        else:
            return self.x <= other and self.y <= other

    def __ge__(self, other):
        if isinstance(other, Point):
            return self.x >= other.x and self.y >= other.y
        else:
            return self.x >= other and self.y >= other

    def __str__(self):
        return "%s (%0.2f, %0.2f)" % (self.name, self.x, self.y)


class BasicPoint(Point):
    pass


class DependPoint(Point):
    def __init__(self, name, parent1, parent2, index=0):
        if isinstance(parent1, Segment):
            if isinstance(parent2, Segment):
                interpoint = parent1.intersection(parent2)
                print(interpoint)
                if interpoint:
                    super().__init__(interpoint.x, interpoint.y)
                self.parent1 = parent1
                self.parent2 = parent2
                self.name = name

            else:
                interpoint = parent2.intersectionSegment(parent1)
                i = interpoint[index]
                super().__init__(i.x, i.y)
                self.parent1 = parent1
                self.parent2 = parent2
                self.name = name
        else:
            if isinstance(point2, Segment):
                interpoint = parent1.intersectionSegment(parent2)
                i = interpoint[index]
                super().__init__(i.x, i.y)
                self.parent1 = parent1
                self.parent2 = parent2
                self.name = name
            else:
                pass
