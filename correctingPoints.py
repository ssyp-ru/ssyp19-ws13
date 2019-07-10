import geom as geometry
def correctingPoints(point, segments, circles):
    error = 4
    for _, i in circles.items():
        list = i.intersectionLine(geometry.Line(i.center, point))
        if not list: 
            return point
        for j in list:
            Fcondition = point.distToPoint(j) < error
            Scondition = point.distToPoint(j) > -error
            print(str(j))
            if Fcondition and Scondition:
                point.x = j.x
                point.y = j.y
    return point