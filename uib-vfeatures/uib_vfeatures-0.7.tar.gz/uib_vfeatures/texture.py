from skimage.feature import greycomatrix, greycoprops
import numpy as np
from scipy import stats
import cv2


class Texture:

    @staticmethod
    def texture_features(image, distances, angles, properties):
        """ Calc the texture properties of a greyscale image

        Calculate the property passed as parameter of the function.

        Refs:
            https://scikit-image.org/docs/0.7.0/api/skimage.feature.texture.html

        Args:
            distances: List of pixel pair distance offsets
            angles: List of pixel pair angles in radians.
            properties: Array of Strings. The feature that you want to calculate. 'contrast',
                        'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation'.
            image: Greyscale image in uint8
        Returns:
            Array of float. The texture properties of the image.
        """
        glcm = greycomatrix(image, distances=distances, angles=angles, symmetric=True, normed=True)

        return np.hstack([greycoprops(glcm, prop).ravel() for prop in properties])

    @staticmethod
    def skew(img):
        """ Calculate the skew of an image

        The skew is the difference between the mean and the median of the image. And is a measure of
        the asymmetry of the image.

        Args:
            img: Numpy array of uint8

        Returns:
            The skew of the image.
        """
        img_histogram = cv2.calcHist([img], [0], None, [256], [0, 256])

        return stats.skew(img_histogram)

    @staticmethod
    def kurtosis(img):
        """ Calculate the kurtosis of an image.

        The kurtosis is the difference between the mean and the median of the image. And is a
        measure of the asymmetry of the image.

        Args:
            img: Numpy array of uint8

        Returns:
            The kurtosis of the image.
        """
        img_histogram = cv2.calcHist([img], [0], None, [256], [0, 256])

        return stats.kurtosis(img_histogram)
