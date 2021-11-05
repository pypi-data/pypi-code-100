# -*- coding: utf-8 -*-
""" Module for color related features.

This package contains functions for color related features.

Written by: Miquel Miró Nicolau (UIB)
"""
from copy import copy

import cv2
import numpy as np
from sklearn import cluster


class Color:
    """ Class for color related features. """

    @staticmethod
    def mean_sdv_lab(img, channel=0):
        """ Calc the mean an the standard desviation of a channel of a RGB image

        Args:
            img: Image with three channels
            channel: Id of the channel to calculate the mean and the standard desviation
        Returns:
            Mean and standard desviation of the channel in LAB
        """
        img_lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

        return Color.mean_sdv(img_lab, channel)

    @staticmethod
    def mean_sdv_rgb(img, channel=0):
        """ Calc the mean an the standard desviation of a channel of a RGB image

        Args:
            img: Image with three channels
            channel: Id of the channel to calculate the mean and the standard desviation

        Returns:
            Mean and standard desviation of the channel in RGB
        """
        return Color.mean_sdv(img, channel)

    @staticmethod
    def mean_sdv_hsv(img, channel=0):
        """ Calc the mean an the standard desviation of a channel of a RGB image

        Args:
            img: Image with three channels
            channel: Id of the channel to calculate the mean and the standard desviation
        Returns:
            Mean and standard desviation of the channel in HSV
        """

        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        return Color.mean_sdv(img_hsv, channel)

    @staticmethod
    def mean_sdv(img, channel=0):
        """ Calc the mean an the standard desviation of a channel of an image

        Args:
            img: Image with three channels
            channel: Id of the channel to calculate the mean and the standard desviation

        Returns:
            Mean and standard desviation of the channel
        """
        if channel != 0:
            channel = cv2.split(img)[channel - 1]
        else:
            channel = copy(img)

        return cv2.meanStdDev(channel)

    @staticmethod
    def dominant_colors(image: np.ndarray, mask: np.ndarray, n_colors: int,
                        random_start: int = 42):
        """ Get the dominant colors of an image

        Args:
            image: Numpy array of a color image
            mask: Numpy array of a binary image
            n_colors: Number of colors to return
            random_start: Random seed for the kmeans algorithm

        Returns:
            A list of colors corresponding to the dominant colors of the image
        """
        hue, saturation, value = cv2.split(image)

        train = []

        for coord_x in range(0, hue.shape[0]):
            for coord_y in range(0, hue.shape[1]):
                if mask[coord_x][coord_y] == 1:
                    if train is None:
                        train = np.array([hue[coord_x][coord_y], saturation[coord_x][coord_y],
                                          value[coord_x][coord_y]])
                    else:
                        train.append(np.array([hue[coord_x][coord_y], saturation[coord_x][coord_y],
                                               value[coord_x][coord_y]]))

        kmeans = cluster.KMeans(n_clusters=n_colors, random_state=random_start)
        clusters = kmeans.fit_predict(np.array(train))

        _, importance = np.unique(clusters, return_counts=True)

        importance = importance / sum(importance)

        return zip(kmeans.cluster_centers_, importance)

    @staticmethod
    def color_bins(image: np.ndarray, mask: np.ndarray, n_colors: int):
        """ Calculate the color bins of an image

        Color bins are the dominant colors of the image divided in n_colors bins. For each channel,
        the color bins are calculated as the mean of the dominant colors of the image.

        Args:
            image: Numpy array of a color image
            mask: Numpy array of a binary image
            n_colors: Integer number of color bins for each channel

        Returns:
            A list of color bins for each channel concatenated.
        """
        channels = cv2.split(image)
        histograms = [np.histogram(c[mask], bins=n_colors)[0] for c in channels]

        return np.hstack(histograms)
