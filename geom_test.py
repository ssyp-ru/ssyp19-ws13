import geom
import math

Apoint = geom.Point(10, 0)
Bpoint = geom.Point(1, 1)
Cpoint = geom.Point(11, 1)
Dpoint = geom.Point(25, 5)
Epoint = geom.Point(7, 1)
Avector = geom.Vector(Apoint)
Bvector = geom.Vector(Bpoint)
angle = math.degrees(math.acos(Avector.angle(Bvector)))
Nvector = Bvector.singleDirectedVector()
BprojectionA = Avector.projection(Bvector)
Sparallelogram = Avector.crossProduct(Bvector)
NewStraight = geom.Straight(Apoint, Cpoint)
NewSegment = geom.Segment(Bpoint, Cpoint)
assert (1 - Avector.length) < 10 ** -9
assert (45 - angle) < 10 ** -9
assert (1 - Nvector.length) < 10 ** -9
assert (1 - BprojectionA.length) < 10 ** -9
assert (10 - Sparallelogram) < 10 ** -9
assert NewStraight.isPointBelongs(Dpoint) == False 
assert (5 - NewSegment.length) < 10 ** -9
assert NewSegment.isPointBelongs(Epoint)

