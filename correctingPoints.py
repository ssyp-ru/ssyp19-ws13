import geom as geometry
def correctingPoints(point, segments, circles):
    error = 8
    for _, i in circles.items():
        list = i.intersectionLine(geometry.Line(i.center, point))
        if not list: 
            return point
        for j in list:
            condition = -error <= point - j <= error
            if condition:
                point.x = j.x
                point.y = j.y
    for _, i in segments.items():
        if point.distToSegment(i) < error:
            return point.projectionOnSegment(i)
    return point