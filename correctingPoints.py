import geom as geometry
import math

def correctingPoints(point, segments, circles):
    error = 8
    for _, circle in circles.items():
        dist = math.hypot(point.x-circle.center.x, point.y-circle.center.y)
        if -error < dist - circle.radius <= error:
            radialLine = geometry.Line(circle.center, point)
            list = circle.intersectionLine(radialLine)
            closest = min(list, key = lambda x: math.hypot(x.x-point.x, x.y-point.y))
            point = closest
            return point
    for _, i in segments.items():
        if point.distToSegment(i) < error:
            return point.projectionOnSegment(i)
    return point