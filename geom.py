import math


class StraightError(ValueError):
	pass

class Point:
	def distToPoint(self, point):
		X = self.x - point.x
		Y = self.y - point.y
		return math.sqrt((X ** 2) + (Y ** 2))
	def	distToStraight(self, straight):
		inclined = Vector(Point(straight.point1.x - self.x, straight.point1.y - self.y))
		cross = inclined.crossProduct(Vector(Point(straight.point2.x - straight.point1.x, straight.point2.y - straight.point1.y)))
		return abs((cross * 2) / Vector(Point(straight.point2.x - straight.point1.x, straight.point2.y - straight.point1.y)).length)
	def __init__ (self, x, y):
		self.x = x
		self.y = y

class Segment():

	def isPointBelongs(self, point):
		if (point.distToPoint(self.point1) + point.distToPoint(self.point2) == self.point1.distToPoint(self.point2)):
			return True
		else:
			return False
	def intersection(self, segment):
		Mstraight = Straight(self.point1, self.point2)
		interpoint = Mstraight.intersection(Straight(segment.point1, segment.point2))
		if (self.isPointBelongs(interpoint) and segment.isPointBelongs(interpoint)):
			return interpoint
		else:
			return False 
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2
		self.length = point1.distToPoint(point2)

class Straight():

	def isPointBelongs(self, point):
		if ((point.x == self.point1.x and point.y == self.point1.y ) or (point.x == self.point2.x and point.y == self.point2.y)):
			return True
		ABvector = Vector(Point(self.point2.x - self.point1.x, self.point2.y - self.point1.y))
		ACvector = Vector(Point(point.x - self.point1.y, point.y - self.point1.y))
		if (ABvector.crossProduct(ACvector) == 0):
			return True
		else:
			return False

	def intersection(self, straight):
		if (((self.A * straight.B) - (self.B * straight.A)) == 0):
			return False
		else:
			return (Point(((self.C * straight.B) - (self.B * straight.C)) / ((self.A * straight.B) - (self.B * straight.A)), 
						((self.A * straight.C) - (self.C * straight.A)) / ((self.A * straight.B) - (self.B * straight.A))))
	def __init__(self, point1, point2):
		if ((point1.x == point2.x) and (point1.y == point2.y)):	
			raise(StraightError("That points are the same"))
		else:
			self.point1 = point1
			self.point2 = point2
			self.A = -(point2.y - point1.y)
			self.B = point2.x - point1.x
			Nvector = Vector(Point(self.A, self.B))
			self.C = Nvector.dotproduct(Vector(Point(point2.x, point2.y)))

class Vector :
	def dotproduct(self, vector):
		return (self.x * vector.x) + (self.y * vector.y)
	def angle(self, vector):
		multiplied = self.dotproduct(vector)
		return math.degrees(math.acos(multiplied / (self.length * vector.length)))
	def projection (self, vector):
		Nvector = self.singleDirectedVector()
		return Nvector.__productVecByNum__(Nvector.dotproduct(vector))
	def __productVecByNum__(self, num):
		return Vector(Point(self.x * num, self.y * num))
	def singleDirectedVector(self):
		return Vector(Point((self.x / self. length), (self.y / self.length)))
	def crossProduct(self, vector):
		return (self.x * vector.y) - (vector.x * self.y)
	def __init__ (self, point):
		self.x = point.x
		self.y = point.y
		point00 = Point(0, 0)
		self.length = point00.distToPoint(point)

