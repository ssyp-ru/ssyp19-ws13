import math


class StraightError(ValueError):
	pass

class Point:
	def dist (self, point):
		X = self.x - point.x
		Y = self.y - point.y
		return math.sqrt((X ** 2) + (Y ** 2))

	def __init__ (self, x, y):
		self.x = x
		self.y = y

class Segment():

	def isPointBelongs(self, point):
		if (point.dist(self.point1) + point.dist(self.point2) == self.point1.dist(self.point2)):
			return True
		else:
			return False
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2
		self.length = point1.dist(point2)

class Straight():
	def isPointBelongs(self, point):
		if ((point.x == self.x1 and point.y == self.y1 ) or (point.x == self.x2 and point.y == self.x2)):
			return True
		ABvector = Vector(Point(self.x2 - self.x1, self.y2 - self.y1))
		ACvector = Vector(Point(point.x - self.x1, point.y - self.y1))
		if (ABvector.crossProduct(ACvector) == 0):
			return True
		else:
			return False

	def __init__(self, point1, point2):
		if (point1.x != point2.x and point1.y != point2.y):	
			self.x1 = point1.x
			self.x2 = point2.x
			self.y1 = point1.y
			self.y2 = point2.y
		else:
			raise(StraightError("That points are the same"))

class Vector :
	def product(self, vector):
		return (self.x * vector.x) + (self.y * vector.y)
	def angle(self, vector):
		multiplied = self.product(vector)
		return multiplied / (self.length * vector.length)
	def projection (self, vector):
		Nvector = self.singleDirectedVector()
		return Nvector.__productVecByNum__(Nvector.product(vector))
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
		self.length = point00.dist(point)


