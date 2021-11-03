from unittest import TestCase

from voxypy.models.models import Voxel


class TestVoxel(TestCase):
    def test_set(self):
        v = Voxel(0)
        self.assertEqual(1, v.set(1))
        try:
            v.set(256)
            self.fail("Setting 256 should have failed.")
        except ValueError:
            pass
        except Exception as e:
            self.fail(f"Unexpected exception type {e}")
        try:
            v.set(-1)
            self.fail("Setting -1 should have failed.")
        except ValueError:
            pass
        except Exception as e:
            self.fail(f"Unexpected exception type {e}")

    def test_add(self):
        v = Voxel(0)
        a = int(v.add(1))
        self.assertEqual(0, a)
        v = Voxel(1)
        self.assertEqual(2, int(v.add(1)))
        v = Voxel(255)
        self.assertEqual(1, int(v.add(1)))
        v = Voxel(250)
        self.assertEqual(5, int(v.add(10)))
        v = Voxel(10)
        self.assertEqual(5, int(v.add(-5)))
        v = Voxel(1)
        self.assertEqual(255, int(v.add(-1)))
        v = Voxel(5)
        self.assertEqual(255, int(v.add(-5)))

    def test_subtract(self):
        v = Voxel(0)
        self.assertEqual(0, int(v.subtract(1)))
        v = Voxel(1)
        self.assertEqual(255, int(v.subtract(1)))
