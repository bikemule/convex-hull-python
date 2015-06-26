'''Tests for shapes.py'''

from shapes import Point, Polygon, ccw, intersect


def test_ccw():

    a, b, c = Point(0,0), Point(1,0), Point(1,1)

    print ccw(a,b,c)

    assert ccw(a,b,c) > 0

    a,b,c,d = Point(0,0), Point(5,0), Point(5,5), Point(0,5)

    assert ccw(a,b,c) > 0


def test_is_convex():
    
    square = Polygon([Point(0,0), Point(5,0), Point(5,5), Point(0,5)])

    assert square.is_convex() == True


def test_poly_intersect():
    
    square = Polygon([Point(0,0), Point(5,0), Point(5,5), Point(0,5)])
    intersecting_sq = Polygon([Point(1,1), Point(6,1), Point(6,6), Point(1,6)])
    
    assert square.intersects(intersecting_sq) == True


def test_intersect():

    l1, l2 = (Point(0,0), Point(0,10)), (Point(-1,-1), Point(1,1))
    l3     = (Point(20,20), Point(30,30))

    assert intersect(l1, l2) == True


def test_points():
    """Added a test because of the different potential inputs."""

    point12 = Point(1,2)
    point23 = Point([2,3])
    
    assert point12.x == 1
    assert point12.y == 2

    assert point23.x == 2
    assert point23.y == 3


def test_contains_point():

    square = Polygon([Point(0,0), Point(5,0), Point(5,5), Point(0,5)])

    assert square.contains_point(Point(1,1)) == True
    assert square.contains_point(Point(-1,-1)) == False


def test_contains_polygon():

    square = Polygon([Point(0,0), Point(10,0), Point(10,10), Point(0,10)], "Square")
    little_square = Polygon([Point(3,3), Point(6,3), Point(6,6), Point(3,6)], "Lil Sq")

    assert square.contains_polygon(little_square) == True
    assert little_square.contains_polygon(square) == False


def test_inside():
    
    square = Polygon([Point(0,0), Point(10,0), Point(10,10), Point(0,10)], "Square")
    little_square = Polygon([Point(3,3), Point(6,3), Point(6,6), Point(3,6)], "Lil Sq")

    assert square.is_inside(little_square) == False
    assert little_square.is_inside(square) == True

