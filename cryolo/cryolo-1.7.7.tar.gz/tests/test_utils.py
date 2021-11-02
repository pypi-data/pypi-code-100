import unittest

import cryolo.utils

class MyTestCase(unittest.TestCase):
    def test_resample_filament_returns_fila(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=1182, y=2116, w=30, h=30, c = 1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=1248, y=1926, w=30, h=30, c = 1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 10)
        self.assertTrue(res_fil.boxes is not None,"No boxes")

    def test_resample_filament_correct_length(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=0, y=0, w=30, h=30, c = 1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=100, y=0, w=30, h=30, c = 1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 10)
        self.assertEqual(10,len(res_fil.boxes))

    def test_resample_filament_correct_maxx(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=20, y=5, w=30, h=30, c = 1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=85, y=35, w=30, h=30, c = 1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 6)
        for b in res_fil.boxes:
            print(b.x,b.y)
        self.assertTrue(res_fil.boxes[-1].x <= 85)
        self.assertTrue(res_fil.boxes[0].x >= 20)
        self.assertTrue(res_fil.boxes[-1].y <= 35)
        self.assertTrue(res_fil.boxes[0].y >= 5)


if __name__ == '__main__':
    unittest.main()
