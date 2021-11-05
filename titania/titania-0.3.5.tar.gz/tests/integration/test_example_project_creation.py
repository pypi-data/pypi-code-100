import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # create project
        project_name = "test_project"
        result = os.system("python -m core start --name %s" % project_name)
        self.assertEqual(result, 0)

        # assert project_name ingredients
        self.assertTrue(os.path.isdir('%s' % project_name))
        self.assertTrue(os.path.isdir('%s/data' % project_name))
        self.assertTrue(os.path.isdir('%s/panels' % project_name))
        self.assertTrue(os.path.isdir('%s/plots' % project_name))
        self.assertTrue(os.path.isdir('%s/views' % project_name))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s/data' % project_name, '__init__.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s/panels' % project_name, '__init__.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s/panels' % project_name, 'control_panel.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s/plots' % project_name, '__init__.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s/views' % project_name, 'thresholds.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s/views' % project_name, 'thresholds_gui.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s' % project_name, '__init__.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s' % project_name, 'config.py')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), '%s' % project_name, 'main.py')))

        # delete project
        result = os.system("rm -rf test_project")
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
