import logging
from heapq import heappush, heapify, heappop
from shapely.geometry import GeometryCollection

from bst import AVLTree, Node
from models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SweepLine:
    def __init__(self):
        self.result = []
        self.event_points = []

    def handle_event_point(self, ep):
        raise NotImplementedError
    
    def run(self):
        logger.info("sweep line started")
        while(len(self.event_points)):
            logger.info(f" Q:\n{self.event_points}")
            self.handle_event_point(heappop(self.event_points))
        return self.result


class BentleyOttmann(SweepLine):

    def __init__(self, segment_cordinate_list):
        """
        :param segment_cordinate_list: list of cordiantes like [ ((x11,y11), (x12,y12)), ... ]
        """
        super().__init__()
        self.t = AVLTree()
        for segment_cor in segment_cordinate_list:
            start_point = Point(segment_cor[0])
            end_point = Point(segment_cor[1])
            segment = Segment([start_point, end_point])
            start_point.set_segment(segment, is_start_point=True)
            end_point.set_segment(segment, is_start_point=False)
            heappush(self.event_points, start_point)
            heappush(self.event_points, end_point)

    def add_intersect(self, seg1, seg2, sx):
        if seg1 is None or seg2 is None:
            return
        if isinstance(seg1, Node):
            seg1 = seg1.key
        if isinstance(seg2, Node):
            seg2 = seg2.key
        if seg1.intersects(seg2):
            cross_point = Point(seg1.intersection(seg2))
            cross_point.set_cross_segment(seg1, seg2)
            if cross_point.x <= sx:
                logger.info(f"add ignored {cross_point}")
                return None
            heappush(self.event_points, cross_point)
            logger.info(f"add {cross_point}")
            return cross_point
        return None

    def remove_intersect(self, seg1, seg2, sx):
        if seg1 is None or seg2 is None:
            return
        if isinstance(seg1, Node):
            seg1 = seg1.key
        if isinstance(seg2, Node):
            seg2 = seg2.key
        if seg1.intersects(seg2):
            # by using heap, this takes: O(n)
            cross_point = seg1.intersection(seg2)
            if cross_point.x <= sx:
                logger.info(f"remove ignored {cross_point}")
                return None
            logger.info(f"remove {cross_point}")
            try:
                self.event_points.remove(cross_point)
                return cross_point
            except Exception as e:
                logger.info(f"NOT FOUND")
            heapify(self.event_points)
        return None

    def handle_event_point(self, p):
        logger.info("handling p: "+str(p)+" with relation "+ str(p.segment_relation))
        logger.info(" T:\n"+str(self.t))
        self.t.sweep_line_x = p.x
        if p.segment_relation == Relation.start_endpoint:
            segment_node = self.t.insert(p.segment)
            left_segment_node = self.t.get_left(segment_node)
            right_segment_node = self.t.get_right(segment_node)
            self.remove_intersect(left_segment_node, right_segment_node, p.x)
            self.add_intersect(p.segment, left_segment_node, p.x)
            self.add_intersect(p.segment, right_segment_node, p.x)

        elif p.segment_relation == Relation.end_endpoint:
            segment_node = self.t.find(p.segment)
            left_segment_node = self.t.get_left(segment_node)
            right_segment_node = self.t.get_right(segment_node)
            self.t.remove_by_node(segment_node)
            self.add_intersect(left_segment_node, right_segment_node, p.x)

        elif p.segment_relation == Relation.cross_point:
            self.result.append((p.x, p.y))
            segment1_node = self.t.find(p.segment)
            segment2_node = self.t.find(p.cross_segment)
            left_segment_node = self.t.get_left(segment1_node)
            right_segment_node = self.t.get_right(segment2_node)
            self.remove_intersect(right_segment_node, segment2_node, p.x)
            self.remove_intersect(left_segment_node, segment1_node, p.x)
            self.add_intersect(right_segment_node, segment1_node, p.x)
            self.add_intersect(left_segment_node, segment2_node, p.x)
            segment1_node.key, segment2_node.key = segment2_node.key, segment1_node.key
            