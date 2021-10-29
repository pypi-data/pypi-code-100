import copy

from unittest import TestCase

from road_collisions.utils import epsg_900913_to_4326


class UtilsTest(TestCase):

    def test_epsg_900913_to_4326(self):
        self.assertEqual(
            epsg_900913_to_4326(-697459.30722, 7042917.21888),
            (-6.265383558143537, 53.32272161460827)
        )
