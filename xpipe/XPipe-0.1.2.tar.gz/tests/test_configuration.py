from unittest import TestCase, mock

from os.path import dirname, realpath, join
from xpipe.config import load_config
import numpy as np
import os

class TestConfiguration(TestCase):

    def setUp(self):
        dir_path = dirname(realpath(__file__))
        self.conf = load_config(join(dir_path, "./resources/template.yaml"))

    def test_eq(self):
        self.assertEqual(self.conf, self.conf)
        self.assertEqual(self.conf.training, self.conf.training)
        self.assertNotEqual(self.conf, self.conf.training)

    def test_get_integer(self):
        self.assertEqual(
            self.conf.training.batch_size(), 
            10
        )

    def test_get_list(self):
        l = self.conf.training.classes()
        self.assertIsInstance(l, list)
        self.assertListEqual(l, [0,1,2,3,4])

    def test_instantiate_object(self):
        ar = self.conf.training.obj()
        self.assertIsInstance(ar, np.ndarray)
        self.assertListEqual(list(ar), [1,2])

    def test_get_object_parameter(self):
        self.assertListEqual(
            self.conf.training.obj._params.object(), 
            [1, 2]
        )

    def test_instantiate_list_objects(self):
        objects_list = self.conf.data.transforms()
        self.assertListEqual(list(objects_list[0]), [1, 2])
        self.assertListEqual(list(objects_list[1]), [2, 3])
        self.assertEqual(len(objects_list), 4)
    
    def test_include(self):
        a = self.conf.inc.a()
        self.assertEqual(a, 1)
        self.assertTrue(len(self.conf.inc.user()))
        self.assertListEqual(self.conf.inc.inc.object(), [1,2,3,4])
        
    
    def test_include_obj(self):
        a = self.conf.obj_include()
        self.assertListEqual(list(a), [1,2,3,4])

    def test_double_star(self):
        def test(batch_size, obj, classes, **kwargs):
            self.assertEqual(batch_size(), 10)
            self.assertListEqual(list(obj._params.object()), [1,2])
        a = self.conf.training
        test(**a)

    def test_env_var(self):
        a = self.conf.user()
        self.assertTrue(len(a))
    
    def test_str_fmt(self):
        a = self.conf.str_fmt()
        self.assertTrue(len(a))
