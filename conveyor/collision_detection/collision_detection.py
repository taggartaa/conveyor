from shapes import Rectangle
from conveyor.math import Vector

class RectangleCollisionDetectorNoRotation(object):      
    @staticmethod
    def _get_rects(parms):
        rects = []
        for parm in parms:
            if isinstance(parm, Rectangle):
                rects.append(parm)
            else:
                rects.append(parm.rect)
                
        return rects
    
    @staticmethod
    def intersection(parm1, parm2):
        rect1, rect2 = RectangleCollisionDetectorNoRotation._get_rects([parm1, parm2])
        
        right_most_left_side = max(rect1.left, rect2.left)
        left_most_right_side = min(rect1.right, rect2.right)
        bottom_most_top_side = max(rect1.top, rect2.top)
        top_most_bottom_side = min(rect1.bottom, rect2.bottom)

        # If the left most ride side is left of the right most left side, no intersection
        if left_most_right_side <= right_most_left_side:
            return None
        # If the bottom most top side is below the top most bottom side, no intersection
        elif bottom_most_top_side >= top_most_bottom_side:
            return None
        else:
            return Rectangle(x = right_most_left_side,
                             y = bottom_most_top_side,
                             width = left_most_right_side - right_most_left_side,
                             height = top_most_bottom_side - bottom_most_top_side)
                             
    @staticmethod
    def contains(parm1, parm2):
        rect1, rect2 = RectangleCollisionDetectorNoRotation._get_rects([parm1, parm2])
        
        