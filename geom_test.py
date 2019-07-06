import geom
import math

Avector = geom.Vector(10, 0)
Bvector = geom.Vector(1, 1)
angle = math.degrees(math.acos(Avector.angle(Bvector)))
Nvector = Bvector.singleDirectedVector()
BprojectionA = Avector.projection(Bvector)
Sparallelogram = Avector.crossProduct(Bvector)
assert (1 - Avector.length) < 10 ** -9
assert (45 - angle) < 10 ** -9
assert (1 - Nvector.length) < 10 ** -9
assert (1 - BprojectionA.length) < 10 ** -9
assert (10 - Sparallelogram) < 10 ** -9

