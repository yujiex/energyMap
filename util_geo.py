# geometry calculation

def dot((x0, y0), (x1, y1)):
    return (x0*x1) + (y0*y1)
def test_dot():
    assert(dot((0, 1), (1, 1)) == 1)
    assert(dot((-1, 1), (1, 1)) == 0)
    assert(dot((3, 5), (1, 1)) == 8)

def cross((x0, y0), (x1, y1)):
    return (x0*y1) - (y0*x1)
def test_cross():
    assert(cross((0, 1), (1, 1)) == -1)
    assert(cross((-1, 1), (1, 1)) == -2)
    assert(cross((3, 5), (1, 1)) == -2)

def vminus((x0, y0), (x1, y1)):
    return (x1 - x0, y1 - y0)
def test_vminus():
    assert(vminus((0, 1), (1, 1)) == (1, 0))
    assert(vminus((-1, 1), (1, 1)) == (2, 0))
    assert(vminus((3, 5), (1, 1)) == (-2, -4))

def vplus((x0, y0), (x1, y1)):
    return (x1 + x0, y1 + y0)
def test_vplus():
    assert(vplus((0, 1), (1, 1)) == (1, 2))
    assert(vplus((-1, 1), (1, 1)) == (0, 2))
    assert(vplus((3, 5), (1, 1)) == (4, 6))

def lineSide(p1, p2, p3):
    v2 = vminus(p1, p2)
    v3 = vminus(p1, p3)
    cp = cross(v2, v3)
    if cp > 0:
        return "LEFT"
    if cp < 0:
        return "RIGHT"
    else:
        return "ON"
def test_lineSide():
    assert(lineSide((-1, 1), (0, 0), (0, 1)) == "LEFT")
    assert(lineSide((0, 0.5), (0, 0), (0, 1)) == "ON")
    assert(lineSide((1, 1), (0, 0), (0, 1)) == "RIGHT")

# antiClockwise
def inAngle(p, p1, p2, p3):
    return (lineSide(p1, p2, p) != "LEFT" and 
            lineSide(p1, p3, p) != "RIGHT")
def test_inAngle():
    assert(inAngle((0, 1), (0, 0), (-1, 1), (1, 1)))
    assert(not inAngle((75, 84), (211, 225), (228, 224), (227, 247)))

def isClockWise(points):
    assert(len(points) >= 3)
    return (lineSide(points[2], points[0], points[1]) ==
"RIGHT")
def test_isClockWise():
    assert(isClockWise([(-1, 1), (1, 1), (1, -1), (-1, -1)]))
    assert(not isClockWise([(-1, -1), (1, -1), (1, 1), (-1, 1)]))
    points = [(211, 225), (228, 224), (227, 247), (212, 246)]
    assert(not isClockWise(points))

def pointInPolygon(p, polygonCord):
    length = len(polygonCord)
    points = [(polygonCord[2*i], polygonCord[2*i+1]) for i in
              range(length//2)]
    if isClockWise(points): 
        if not inAngle(p, points[0], points[1], points[-1]):
            return False
        for i in range(1, len(points) - 1):
            if not inAngle(p, points[i], points[i+1], points[i-1]):
                print('{0} not in {1},{2},{3}'.format(p, points[i], points[i+1], points[i-1]))
                return False
    else:
        if not inAngle(p, points[0], points[-1], points[1]):
            return False
        for i in range(1, len(points) - 1):
            if not inAngle(p, points[i], points[i-1], points[i+1]):
                return False
    return True

def test_pointInPolygon():
    '''
    polygonCord = [-1, 1, 1, 1, 1, -1, -1, -1]
    assert(pointInPolygon((0, 0), polygonCord))
    '''
    polygonCord = [211, 225, 228, 224, 227, 247, 212, 246]
    assert(not pointInPolygon((75, 84), polygonCord))

def main():
    test_dot()
    test_cross()
    test_vminus()
    test_vplus()
    test_lineSide()
    test_isClockWise()
#   test_pointInPolygon()
#main()
