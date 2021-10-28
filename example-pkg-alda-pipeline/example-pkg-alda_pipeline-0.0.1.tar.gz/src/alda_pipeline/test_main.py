import unittest
import traceback


from Project import Project


class unitTest(unittest.TestCase):
    def test_adj(self):
        try:
            print('Downloading...')
            main = Project()
            adj = main.get_data_adj()
            print(adj)
            self.assertEqual(adj.tolist(), adj.tolist())
        except:
            print('fail 1')
            traceback.print_exc()
            self.fail()

    def test_volume(self):
        try:
            print('Downloading...')
            main = Project()
            vol = main.get_data_volume()
            self.assertEqual(vol.tolist(), vol.tolist())
        except:
            print('fail 2')
            traceback.print_exc()
            self.fail()


if __name__ == '__main__':
    unittest.main()
