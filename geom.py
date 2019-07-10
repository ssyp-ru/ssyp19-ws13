import math
# from Translator import Translator
# translator = Translator()

class LineError(ValueError):
    pass

class Circle:
    def intersectionLine(self, line):
        # line.normalVector()
        C = line.C + line.A * self.center.x + line.B * self.center.y 
        Acoefficient = line.B * line.B + line.A * line.A 
        Bcoefficient = 2 * line.A * C 
        Ccoefficient = C * C - line.B * line.B * self.radius * self.radius 
        Discriminant = Bcoefficient * Bcoefficient - (4 * Acoefficient * Ccoefficient) 
        if Discriminant < 0:
            return
        y1 = (-Bcoefficient - math.sqrt(Discriminant)) / (2 * Acoefficient) 
        y2 = (-Bcoefficient + math.sqrt(Discriminant)) / (2 * Acoefficient)  
        x1 = (-C - y1 * line.B) / line.A 
        x2 = (-C - y2 * line.B) / line.A
        return [Point(x1 + self.center.x, y1 + self.center.y), Point(x2 + self.center.x, y2 + self.center.y)]

    def __init__(self, point, radius):
        self.center = point
        self.radius = radius
        print("DEBUG>>", self.center, self.radius, type(self.center))
    def __str__(self):
        return f"A circle centered at ({str(self.center)}) with radius {self.radius}"

class Segment():
    def pointBelongs(self, point):
        return point.distToPoint(self.point1) + point.distToPoint(self.point2) <= self.point1.distToPoint(self.point2) + 1

    def intersection(self, segment):
        Mline = Line(self.point1, self.point2)
        interpoint = Mline.intersection(Line(segment.point1, segment.point2))
        if ((interpoint != False) and self.pointBelongs(interpoint) and segment.pointBelongs(interpoint)):
            return interpoint
        else:
            return 

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = point1.distToPoint(point2)
    def __str__(self):
        return f"({str(self.point1)}; {str(self.point2)})"

class Line():
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
        return ABvector.crossProduct(ACvector) == 0

    def intersection(self, line):
        Avector = Vector(self.A, line.B)
        if (Avector.crossProduct(Vector(self.B, line.A)) == 0):
            return False
        else:
            denom = ((self.A * line.B) - (self.B * line.A))
            Fnumerator = ((self.C * line.B) - (self.B * line.C))
            Snumerator = (self.A * line.C) - (self.C * line.A)
            return Point( Fnumerator / denom, Snumerator / denom)

    def __init__(self, point1, point2):
        if ((point1.x == point2.x) and (point1.y == point2.y)):    
            raise(LineError("That points are the same"))
        else:
            self.point1 = point1
            self.point2 = point2
            self.A = point2.y - point1.y
            self.B = -(point2.x - point1.x)
            Nvector = Vector(self.A, self.B)
            self.C = Nvector.dotproduct(Vector(point1.x, point1.y))
            self.normalize()
    def __str__(self):
        return "%0.4f x + %0.4f y + %0.4f = 0" % (self.A, self.B, self.C)    

class Vector:
    def dotproduct(self, vector):
        return (self.x * vector.x) + (self.y * vector.y)

    def angle(self, vector):
        multiplied = self.dotproduct(vector)
        return math.degrees(math.acos(multiplied / (self.length * vector.length)))

    def projection(self, vector):
        Nvector = self.singleDirectedVector()
        return Nvector.__productVecByNum__(Nvector.dotproduct(vector))

    def __productVecByNum__(self, num):
        return Vector(self.x * num, self.y * num)

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
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __str__(self):
        return f"({self.x}, {self.y})"

class Point(Vector):
    def isInCircle(self, circleslist):
        for i in circleslist:
            if (self.distToPoint(circleslist[i].center) < circleslist[i].radius):
                pass
                #translator.connector.call(...)
                #Here i need Vsevolod's code for request in prolog

    def distToPoint(self, point):
        return (self - point).length

    def distToLine(self, line):
        inclined = Vector(line.point1.x - self.x, line.point1.y - self.y)
        cross = inclined.crossProduct(Vector(line.point2.x - line.point1.x, line.point2.y - line.point1.y))
        return abs(cross  / Vector(line.point2.x - line.point1.x, line.point2.y - line.point1.y)).length

    def distToSegment(self, segment):
        inclined = Vector(self.x - segment.point1.x, self.y - segment.point1.y)
        if (inclined.dotproduct(Vector(segment.point2.x - segment.point1.x, segment.point2.y - segment.point1.y))) < 0:
            return (min(self.distToPoint(segment.point1), self.distToPoint(segment.point2)))
        else:
            return self.distToline(segment)

    def __init__ (self, x, y):
        self.x = x
        self.y = y