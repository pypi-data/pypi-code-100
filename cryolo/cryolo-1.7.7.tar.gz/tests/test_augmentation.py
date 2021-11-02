import unittest
import numpy as np
import random
import time
from cryolo.augmentation import Augmentation

class AugTest(unittest.TestCase):

    def test_image_augmentation_time(self):
        np.random.seed(6)
        random.seed(10)
        img = np.random.random_sample(size=(4096, 4096))*255
        img = img.astype(np.uint8)
        img = img.astype(np.float32)
        start = time.time()
        aug = Augmentation(True)
        for i in range(10):
            aug.image_augmentation(img.copy())
            #aug.gauss_blur(img.copy())
            #print img.dtype
        end = time.time()

    def test_sharpen_float32(self):
        np.random.seed(6)
        random.seed(10)
        img = np.random.random_sample(size=(100, 100))*255
        img = img.astype(np.uint8)
        img = img.astype(np.float32)
        aug = Augmentation()
        result = aug.gauss_blur(img.copy())


    def test_image_augmentation_float32(self):
        np.random.seed(6)
        random.seed(10)
        img = np.random.random_sample(size=(10, 10))
        img = img.astype(np.float32)
        aug = Augmentation()
        result = aug.image_augmentation(img.copy())
        is_float = np.issubdtype(result.dtype, np.float32)
        self.assertTrue(is_float, "Image augmentation failed. Type is not correct")

    def test_image_augmentation_uint8(self):
        np.random.seed(7)
        random.seed(10)
        img = np.random.random_integers(0, 255, size=(10, 10))
        img = img.astype(np.float32)
        aug = Augmentation(True)
        result = aug.image_augmentation(img.copy())
        is_int = np.issubdtype(result.dtype, np.uint8)
        self.assertTrue(is_int, "Image augmentation failed. Type is not correct")


    def test_additive_gauss_noise_typecheck_float32(self):
        img = np.random.random_sample(size=(3, 3))
        img = img.astype(np.float32)
        aug = Augmentation()
        result = aug.additive_gauss_noise(img.copy())
        is_float = np.issubdtype(result.dtype, np.float32)
        self.assertTrue(is_float, "ADD GAUSS NOISE FLOAT32 failed. Type is not correct")


    def test_avg_blur_float32(self):
        np.random.seed(7)
        img = np.random.random_sample(size=(3,3))
        img = img.astype(np.float32)
        aug = Augmentation()
        result = aug.avg_blur(img.copy(), kernel_size=(3,4))
        t = np.allclose(np.mean(img), result[1, 1], atol=0.0001)
        self.assertTrue(t, "AVG BLUR FLOAT32 failed.")
        is_float = np.issubdtype(result.dtype, np.float32)
        self.assertTrue(is_float, "AVG BLUR FLOAT32 failed. Type is not correct")


    def test_avg_blur_uint8(self):
        np.random.seed(7)
        img = np.random.random_integers(0,255,size=(3,3))
        print(img)
        img = img.astype(np.uint8)
        aug = Augmentation(True)
        result = aug.avg_blur(img.copy(), kernel_size=(3,4))
        self.assertEqual(140, result[1, 1])
        is_int = np.issubdtype(result.dtype, np.uint8)
        self.assertTrue(is_int, "Avg blurring failed. Type is not correct")


    def test_gaussian_blur_float32(self):
        np.random.seed(7)
        img = np.random.random_sample(size=(3,3))
        aug = Augmentation()
        result = aug.gauss_blur(img.copy())
        print(result)
        img_exp = [[0.3956204, 0.45140969, 0.4693832],
                   [0.43998803, 0.44855732, 0.43916815],
                   [0.43967383, 0.40600407, 0.37695657]]
        t = np.allclose(img_exp, result, atol=0.00001)
        self.assertTrue(t, "Gaussian blurring failed")
        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Gaussian blurring failed. Type is not correct")

    def test_gaussian_blur_uint8(self):
        np.random.seed(7)
        img = np.random.random_integers(0,255,size=(3,3))
        img = img.astype(np.float32)
        aug = Augmentation(True)
        result = aug.gauss_blur(img.copy())
        result = result.astype(np.uint8)
        print(result)
        img_exp = [[178, 144,  99], [175, 140, 125], [154, 125, 115]]
        t = np.array_equal(img_exp, result)
        self.assertTrue(t,"Gaussian blurring failed")

        is_int = np.issubdtype(result.dtype, np.integer)

        self.assertTrue(is_int, "Gaussian blurring failed. Type is not correct")

    def test_contrast_normalization_float32(self):
        np.random.seed(9)
        img = np.zeros((3, 3), dtype="float32")
        img[2, 2] = 255
        aug = Augmentation()
        print(img)
        result = aug.contrast_normalization(img.copy())
        print(result)

        img_exp = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 131.46811]])

        t = np.allclose(img_exp, result,atol=0.0001)
        self.assertTrue(t, msg="Contrast normalization failed. Result is not as expected")

        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Contrast normalization failed. Type is not correct")

    def test_contrast_normalization_uint8(self):
        np.random.seed(9)
        img = np.zeros((3, 3), dtype="float32")
        img[2, 2] = 255
        aug = Augmentation(True)
        result = aug.contrast_normalization(img.copy())
        print(result)
        result = result.astype(np.uint8)
        img_exp = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 131]])

        t = np.allclose(img_exp, result,atol=0.0001)

        self.assertTrue(t, msg="Contrast normalization failed. Result is not as expected")


    def test_add_float32(self):
        np.random.seed(10)
        img = np.ones((3, 3), dtype="float32")
        img[0, 0] = 0
        img[2, 2] = 10
        aug = Augmentation()
        result = aug.add(img.copy(), 0.1)
        print(result)
        t = np.array_equal(img+0.46959287, result)
        self.assertTrue(t, msg="Add failed. Result is not as expected")

        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Add failed. Type is not correct")

    def test_add_uint8(self):
        np.random.seed(10)
        img = np.zeros((3, 3), dtype="float32")
        img[2, 2] = 255

        aug = Augmentation(True)
        result = aug.add(img.copy(), 0.1)
        result = np.clip(result,0,255)
        print(result)
        img_exp = img+13.045981748296022
        img_exp[2,2] = 255.
        t = np.array_equal(img_exp, result)

        self.assertTrue(t, msg="Add failed. Result is not as expected")

    def test_multiply_float32(self):
        np.random.seed(10)
        img = np.ones((3, 3), dtype="float32")
        aug = Augmentation()
        result = aug.multiply(img.copy())
        img_exp = img*1.27132064327
        t = np.array_equal(img_exp, result)
        self.assertTrue(t, msg="Float 32 multiplication failed. Result is not as expected")

        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Multiplication failed. Type is not correct")

    def test_multiply_uint8(self):
        np.random.seed(10)
        img = np.ones((3, 3), dtype="float32")
        img = img * 100
        img[2,2] = 250
        aug = Augmentation(True)
        result = aug.multiply(img.copy())
        np.clip(result,0,255,out=result)
        result = result.astype(np.uint8, copy=False)

        img_exp = [[127, 127, 127],
                   [127, 127, 127],
                   [127, 127, 255]]

        t = np.array_equal(img_exp, result)
        self.assertTrue(t, msg="unit8 multiplication failed. Result is not as expected")

        is_int = np.issubdtype(result.dtype, np.uint8)

        self.assertTrue(is_int, "Multiplication failed. Type is not correct")

    def test_dropout_5x5_float32(self):
        np.random.seed(10)
        img = np.ones((6, 6), dtype="float32")
        img[:3,:] = 3
        aug = Augmentation()
        res = aug.dropout(img.copy(), 0.1)
        num_zero_elements = np.sum(res == 2)
        self.assertEqual(3, num_zero_elements,"Dropout test failed.")

        is_float = np.issubdtype(res.dtype, np.float32)

        self.assertTrue(is_float, "Dropout failed. Type is not correct")

    def test_dropout_5x5_uint8(self):
        np.random.seed(10)
        img = np.ones((6, 6), dtype="float32")
        img[:3, :] = 3
        aug = Augmentation(True)
        res = aug.dropout(img.copy(), 0.1)
        num_zero_elements = np.sum(res == 2)
        self.assertEqual(3, num_zero_elements, "Dropout test failed.")

    def test_dropout_10x10_uint8(self):
        np.random.seed(10)
        img = np.ones((10, 10), dtype="float32")
        img[:5, :] = 3
        aug = Augmentation(True)
        res = aug.dropout(img.copy(), 0.1)
        num_zero_elements = np.sum(res == 2)
        self.assertEqual(8, num_zero_elements, "Dropout test failed.")