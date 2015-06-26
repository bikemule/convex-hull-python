'''Program to work with convex polygons.
Michael Buell
'''

import sys
import math
import json


def ccw(pa, pb, pc):
    '''Returns True if the three Points form a counter-clockwise turn.
    Assumes that the points are not collinear.
    '''

    return (pb.x - pa.x) * (pc.y - pa.y) > (pb.y - pa.y) * (pc.x - pa.x)


def intersect(a, b):
    '''Returns True is the two lines intersect.

    Assumes no collinear points.

    Based on the fact that the beginning and ends of the first line will form
    opposite orientations (cw vs ccw) when combined with the two points of the
    other line.

    Args:
    a and b are each a sequence of two Point objects.
    '''

    return ccw(a[0], b[0], b[1]) != ccw(a[1], b[0], b[1]) and \
                                    ccw(a[0], a[1], b[0]) != \
                                    ccw(a[0], a[1], b[1])


class Point:
    '''An pair of integers representing a point that is a vertex of a polygon
    on a coordinate system.
    Includes negative x and y values.
    '''

    def __init__(self, *args):
        '''Constructor can take 2 args or a sequence of length 2,
        i.e. x,y or (x ,y).
        '''

        if len(args) == 1:
            # Second arg should be a sequence of length 2
            self.x = args[0][0]
            self.y = args[0][1]

        elif len(args) == 2:
            # Second and third args are x and y, respectively
            self.x = args[0]
            self.y = args[1]

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Polygon:
    '''A sequence of Points representing a polygon.'''

    def __init__(self, vertices, name=""):
        '''Takes a sequence of Point objects and an optional name.
        Note that points must be in the correct order.
        '''

        self.name = name

        self.vertices = vertices

        self.edges = []  # line segments

        # Loop through points and pair them to create edges.
        for i, v in enumerate(self.vertices):
            try:
                # The points are start and end of an edge.
                self.edges.append((v, self.vertices[i+1]))
            except IndexError:
                # Last point connects back to the beginning.
                self.edges.append((v, self.vertices[0]))

    def __str__(self):
        return str([str(x) for x in self.vertices])

    def contains_point(self, p):
        '''Returns True if the point is inside this polygon.


        Used this algorithm adapted from C (had to use archive.org):
        http://local.wasp.uwa.edu.au/~pbourke//geometry/insidepoly/

        Args
        p is a Point object
        '''

        v = self.vertices
        inside = False

        p1 = v[0]
        for i in range(1, len(v)):
            p2 = v[i % len(v)]
            if p.y > min(p1.y, p2.y):
                if p.y <= max(p1.y, p2.y):
                    if p.x <= max(p1.x, p2.x):
                        x_intersection = (p.y-p1.y)*(p2.x-p1.x) / (p2.y-p1.y) + p1.x
                        if p1.x == p2.x or p.x <= x_intersection:
                            inside = not inside
            p1 = p2

        return inside

    def contains_polygon(self, polygon):
        '''Returns True if the argument polygon is inside this polygon.'''

        # See if all polygon's vertices are inside this one.
        for point in polygon.vertices:
            if not self.contains_point(point):
                return False

        return True

    def is_inside(self, polygon):
        '''Returns True if this polygon is contained by teh argument polygon.'''

        return polygon.contains_polygon(self)

    def intersects(self, polygon):
        '''Returns True if this polygon intersects the argument polygon.'''

        for i in self.edges:
            for j in polygon.edges:
                if intersect(i, j):
                    return True

        return False

    def is_convex(self):
        '''Returns true if this is a convex polygon, false otherwise.'''

        # First check len > 3
        if len(self.vertices) < 3:
            return False

        # sort points ccw from lowest, left-most point
        verts = self.sort_points_ccw()
        n = len(verts)

        # Adaptation of Wikipedia's Graham Scan algorithm, made less confusing
        for i in range(n):
            if ccw(verts[i % n], verts[(i+1) % n], verts[(i+2) % n]) < 0:
                return False

        return True

    def sort_points_ccw(self):
        '''Return self.vertices ordered started lowest, left-most point and
        going counter-clockwise.
        '''

        # Get point with lowest y-coord
        lowest = sorted(self.vertices, key=lambda p: p.y)[0]

        # See if any other points match it
        lowest_y_candidates = []
        for p in self.vertices:
            if p.y == lowest.y:
                lowest_y_candidates.append(p)

        # If there are ties, take the lowest x val
        if len(lowest_y_candidates) > 1:
            for p in lowest_y_candidates:
                if p.x < lowest.x:
                    lowest = p

        # sorting fails on rectangle example
        ccw_sorted = sorted(self.vertices,
                            key=lambda p: math.atan2(p.y-lowest.y,
                                                     p.x-lowest.x))

        return ccw_sorted


if __name__ == '__main__':

    try:
        shapes_file = open(sys.argv[1], 'r')
    except IndexError:
        print "Not enough arguments. (Missing filename)."
        raise
    except IOError:
        print "Error opening " + sys.argv[1]
        raise

    try:
        shapes_json = json.loads(shapes_file.read())
    except:
        print "Error reading file."
        raise

    shapes = []
    for s in shapes_json["geometry"]["shape"]:
        points = [Point(p["x"], p["y"]) for p in s["point"]]
        shapes.append(Polygon(points, s["id"]))

    for s in shapes:
        list_copy = shapes[:]
        list_copy.remove(s)

        if not s.is_convex():
            print s.name + " is not a convex polygon."
            continue
        for t in list_copy:
            if s.contains_polygon(t):
                print s.name + " surrounds " + t.name + "."
            if s.is_inside(t):
                print s.name + " is inside " + t.name + "."
            if s.intersects(t):
                print s.name + " intersects " + t.name + "."
            if not s.contains_polygon(t) and not s.is_inside(t) \
            and not s.intersects(t):
                print s.name + " is separate from " + t.name + "."
