import math

class Dot:
	def dist (self, x, y):
		X = self.x - x
		Y = self.y - y
		return math.sqrt((X ** 2) + (Y ** 2))

	def __init__ (self, x, y):
		self.x = x
		self.y = y

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
		return Vector(self.x * num, self.y * num)
	def singleDirectedVector(self):
		return Vector((self.x / self. length), (self.y / self.length))
	def crossProduct(self, vector):
		return (self.x * vector.y) + (vector.x * self.y)
	def __init__ (self, x, y):
		self.x = x
		self.y = y
		dot00 = Dot(0, 0)
		self.length = dot00.dist(x, y)


