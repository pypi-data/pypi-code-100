"""
Unit tests.
"""

import os
import unittest

import opennsfw2 as n2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = n2.make_open_nsfw_model()
IMAGE_PATHS = [
    os.path.join(BASE_DIR, "test_image_1.jpg"),
    os.path.join(BASE_DIR, "test_image_2.jpg"),
    os.path.join(BASE_DIR, "test_image_3.jpg"),
]


class TestModel(unittest.TestCase):

    def test_inference_yahoo_preprocessing(self) -> None:
        expected_scores = [0.012, 0.756, 0.067]
        predictions = n2.predict(
            IMAGE_PATHS, preprocessing=n2.Preprocessing.YAHOO
        )
        for expected_score, prediction in zip(expected_scores, predictions):
            score = prediction[1]
            self.assertAlmostEqual(expected_score, score, places=3)

    def test_inference_simple_preprocessing(self) -> None:
        expected_scores = [0.001, 0.597, 0.003]
        predictions = n2.predict(
            IMAGE_PATHS, preprocessing=n2.Preprocessing.SIMPLE
        )
        for expected_score, prediction in zip(expected_scores, predictions):
            score = prediction[1]
            self.assertAlmostEqual(expected_score, score, places=3)
