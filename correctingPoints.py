import geom as geometry
def correctingPoints(point, segments, circles):
    error = 4
    for _, i in circles.items():
        list = i.intersectionLine(geometry.Line(i.center, point))
        if not list: 
            return point
        for j in list:
            condition = -error <= point - j <= error
            if condition:
                point.x = j.x
                point.y = j.y
    return point