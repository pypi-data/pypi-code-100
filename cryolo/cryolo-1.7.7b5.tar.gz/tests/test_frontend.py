import unittest
import os
import pickle
from cryolo.frontend import YOLO
import cryolo.utils as utils
class FrontendTest(unittest.TestCase):


    def test_nms_no_overlapping_boxes(self):
        box = utils.BoundBox(x=10, y=10, w=10, h=10,c=0,classes=[1])
        box2 = utils.BoundBox(x=20, y=20, w=10, h=10,c=0,classes=[1])

        boxes = [box,box2]
        front = YOLO("YOLO", [768, 768], 3, ["p"], 700, [200, 200], backend_weights=None, uniitest=True)
        front.nms_threshold = 0.3
        front.obj_threshold = 0.3
        res = front.non_maxima_suppress_fast(boxes)

        self.assertEqual(len(res), 2)

    def test_nms_two_overlapping(self):
        box = utils.BoundBox(x=10, y=10, w=10, h=10, c=0, classes=[1])
        box2 = utils.BoundBox(x=12, y=12, w=10, h=10, c=0, classes=[1])
        box3 = utils.BoundBox(x=20, y=20, w=10, h=10, c=0, classes=[1])
        box4 = utils.BoundBox(x=22, y=22, w=10, h=10, c=0, classes=[1])

        boxes = [box, box2,box3,box4]
        front = YOLO("YOLO", [768, 768], 3, ["p"], 700, [200, 200], backend_weights=None, uniitest=True)
        front.nms_threshold = 0.3
        front.obj_threshold = 0.3
        res = front.non_maxima_suppress_fast(boxes)

        self.assertEqual(len(res), 2)

if __name__ == '__main__':
    unittest.main()
