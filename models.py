from enum import Enum
from functools import total_ordering

from shapely.geometry import GeometryCollection, LineString
from shapely.geometry import Point as SPoint


class Relation(Enum):
    """
    segment and point realationship types
    """
    nothing = 0
    cross_point = 1
    start_endpoint = 2
    end_endpoint = 3


@total_ordering
class Point(SPoint):
    segment_relation = Relation.nothing
    segment = None

    def set_segment(self, s, is_start_point=True):
        self.segment = s
        if is_start_point:
            self.segment_relation = Relation.start_endpoint
        else:
            self.segment_relation = Relation.end_endpoint
    
    def set_cross_segment(self, s1, s2):
        if s1 > s2:
            s1, s2 = s2, s1
        self.segment = s1
        self.cross_segment = s2
        self.segment_relation = Relation.cross_point

    def __gt__(self, other):
        if self.x > other.x:
            return True
        elif self.x == other.x and self.y > other.y:
            return True
        return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __str__(self):
        return str(self.x)+","+str(self.y)

    def __repr__(self):
        return self.__str__()

@total_ordering
class Segment(LineString):

    def __gt__(self, other):
        max_x = max(self.sx, other.sx)
        self_p = self.find_y(max_x)
        other_p = other.find_y(max_x)
        if self_p.almost_equals(other_p):
            max_x = max(self.coords[0][0], other.coords[0][0])
            self_p = self.find_y(max_x)
            other_p = other.find_y(max_x)
        return self_p.y > other_p.y
    
    def __eq__(self, other):
        if self.almost_equals(other):
            return True
        return False

    def __str__(self):
        return "["+str(self.coords[0]) + "," + str(self.coords[1])+"]"

    def __repr__(self):
        return self.__str__()

    def find_y(self, x):
        hline = LineString([(x,0), (x, max(self.xy[1]))])
        intersection = self.intersection(hline)
        if isinstance(intersection, LineString):
            intersection = Point(intersection.coords[0])
        return intersection
