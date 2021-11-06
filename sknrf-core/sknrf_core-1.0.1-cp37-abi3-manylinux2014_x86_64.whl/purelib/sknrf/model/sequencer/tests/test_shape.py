import unittest
import os

from numpy.testing import *

from sknrf.settings import Settings
from sknrf.model.sequencer._shape import Coordinate, SHAPE, ShapeMap, Grid

__author__ = 'dtbespal'

root = os.sep.join((Settings().root, "model", "sequencer", "tests"))
dg_dir = os.sep.join((Settings().data_root, "datagroups"))
dirname = os.sep.join((Settings().data_root, "testdata"))


class TestShape(unittest.TestCase):
    shape = ShapeMap[SHAPE.TRIANGLE]

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_slope(self):
        self.shape.slope(Coordinate(0, 1, 'W'))

    def test_faces(self):
        self.shape.faces(0, 0)

    def test_corners(self):
        self.shape.corners(Coordinate(0, 0))

    def test_endpoints(self):
        self.shape.endpoints(Coordinate(0, 0, 'N'))
        self.shape.endpoints(Coordinate(0, 0, 'E'))
        self.shape.endpoints(Coordinate(0, 0, 'W'))
        self.shape.endpoints(Coordinate(0, 0, 'S'))

    def test_world_to_vertex_o_vertex_to_world(self):
        i, j, a = Coordinate(0, 10)
        x, y = self.shape.vertex_to_world((i, j, a), scale=10.0)
        i_, j_ = self.shape.world_to_vertex((x, y, a), scale=10.0)
        assert_allclose(i, i_)
        assert_allclose(j, j_)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


class TestGrid(unittest.TestCase):
    shape = ShapeMap[SHAPE.TRIANGLE]

    def setUp(self):
        self.grid = Grid(self.shape, scale=10.0)

    def test_add_face_array(self):
        i_start, i_stop = 0, 10
        j_start, j_stop = 0, 20
        points = (int(abs(i_stop - i_start)), int(abs(j_stop - j_start)))
        self.grid.add_face_array(range(0, points[0]), range(0, points[1]))

    def test_vertex_midpoint(self):
        self.test_add_face_array()
        self.grid.vertex_midpoint(self.grid.faces)


class TestTriangle(TestShape):
    shape = ShapeMap[SHAPE.TRIANGLE]

    def test_slope(self):
        self.shape.slope(Coordinate(0, 1, 'W'))


class TestSquare(TestShape):
    shape = ShapeMap[SHAPE.SQUARE]

    def test_slope(self):
        self.shape.slope(Coordinate(0, 1, 'W'))


class TestRhombus(TestShape):
    shape = ShapeMap[SHAPE.RHOMBUS]

    def test_slope(self):
        self.shape.slope(Coordinate(0, 1, 'W'))


class TestHexagon(TestShape):
    shape = ShapeMap[SHAPE.HEXAGON]

    def test_slope(self):
        self.shape.slope(Coordinate(0, 1, 'E'))

    def test_world_to_vertex_o_vertex_to_world(self):
        super().test_world_to_vertex_o_vertex_to_world()
        i, j, a = Coordinate(0, 10, 'R')
        x, y = self.shape.vertex_to_world((i, j, a), scale=10.0)
        i_, j_ = self.shape.world_to_vertex((x, y, a), scale=10.0)
        assert_allclose(i, i_)
        assert_allclose(j, j_)


def iterator_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestTriangle))
    test_suite.addTest(unittest.makeSuite(TestSquare))
    test_suite.addTest(unittest.makeSuite(TestRhombus))
    test_suite.addTest(unittest.makeSuite(TestHexagon))

    return test_suite


if __name__ == '__main__':
    pass
    # import sys
    # from PySide import QtCore
    # from sknrf.model.base import AbstractModel
    #
    # app = QtCore.QCoreApplication(sys.argv)
    # AbstractModel.init()
    #
    # runner = unittest.TextTestRunner()
    # runner.run(iterator_test_suite())
