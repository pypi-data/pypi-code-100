# -*- coding: utf-8 -*-
""" Module containing the Contours class.

This module contains the Contours class , which is used to handle contours and obtain their
features.

"""

import math

import cv2
import numpy as np


class Contours:
    @staticmethod
    def area(contour):
        """ Calculates the area of the contour.

        Args:
            contour: List of points defining the contour

        Returns:
            Area of the contour
        """
        return cv2.contourArea(contour)

    @staticmethod
    def perimeter(contour):
        """ Calculates the perimeter of the contour.

        Args:
            contour: List of points defining the contour

        Returns:
            Perimeter of the contour
        """
        return cv2.arcLength(contour, True)

    @staticmethod
    def convex_hull(contour):
        """ Calculates the convex hull of the contour.

        This function is used to calculate the convex hull of the contour, using the Sklansky's
        algorithm. This algorithm has a complexity of O(n log n), where n is the number of points in
        the contour.

        Args:
            contour: Input contour with a list of points.

        Returns:
            Convex hull of the contour
        """
        return cv2.convexHull(contour)

    @staticmethod
    def convex_hull_perimeter(contour):
        """ Calculates the perimeter of the convex hull of the contour.

        Args:
            contour: List of points defining the contour

        Returns:
            Perimeter of the convex hull of the contour
        """
        return Contours.perimeter(Contours.convex_hull(contour))

    @staticmethod
    def convex_hull_area(contour):
        """ Calculates the area of the convex hull of the contour.

        Args:
            contour: List of points defining the contour

        Returns:
            Area of the convex hull of the contour
        """
        return cv2.contourArea(Contours.convex_hull(contour))

    @staticmethod
    def _bounding_box(contour):
        """ Calculate the bounding box of a contour.

        Args:
            contour: List of points defining the contour
        Returns:
            Bounding box of the contour
        """
        contours_poly = cv2.approxPolyDP(contour, 3, True)

        return cv2.boundingRect(contours_poly)

    @staticmethod
    def bounding_box_area(contour):
        """ Calculates the area of the bounding box of the contour.

        Args:
            contour: List of points defining the contour

        Returns:
            Area of the bounding box of the contour
        """
        _, _, w, h = Contours._bounding_box(contour)

        return w * h

    @staticmethod
    def rectangularity(contour):
        """ Calculates the rectangularity of the contour.

        Calculates the proportion between the real area of the contour and the bounding box. Ratio
        of area of the object to itsbounding box area

        Args:
            contour: List of points defining the contour

        Returns:

        """
        return Contours.area(contour) / Contours.bounding_box_area(contour)

    @staticmethod
    def max_r(contour):
        """ Calculates the radius of the minimum inscribed circle of the contour.

        Args:
            contour: Contour with a list of points

        Returns:
            Radius of the minimum inscribed circle of the contour
        """
        (_, _), radius = cv2.minEnclosingCircle(contour)
        return radius

    @staticmethod
    def min_r(contour):
        """ Calculates the radius of the minimum inscribed circle of the contour.

        Args:
            contour: Contour with a list of points
        Returns:
            Radius of the minimum inscribed circle of the contour
        """
        _, _, width, height = cv2.boundingRect(contour)
        width = int(width) * 2
        height = int(height) * 2
        raw_distance = np.empty((width, height), dtype=np.float32)
        for i in range(width):
            for j in range(height):
                raw_distance[i, j] = cv2.pointPolygonTest(contour, (j, i), True)
        _, maxVal, _, _ = cv2.minMaxLoc(raw_distance)
        return abs(maxVal)

    @staticmethod
    def major_axis(contour):
        """ Calculates the major axis of the minimum inscribed circle of the contour.

        Args:
            contour: Contour with a list of points

        Returns:
            Major axis of the minimum inscribed circle of the contour
        """
        (_, _), (_, major), _ = cv2.fitEllipse(contour)

        return major

    @staticmethod
    def minor_axis(contour):
        """ Calculates the minor axis of the minimum inscribed circle of the contour.

        Args:
            contour: Contour with a list of points

        Returns:
            Minor axis of the minimum inscribed circle of the contour
        """
        (_, _), (minor, _), _ = cv2.fitEllipse(contour)

        return minor

    @staticmethod
    def orientation(contour):
        """ Calculates the orientation of the minimum inscribed circle of the contour.

        Args:
            contour: Contour with a list of points

        Returns:
            Orientation of the minimum inscribed circle of the contour
        """
        (_, _), (_, _), orientation = cv2.fitEllipse(contour)

        return orientation

    @staticmethod
    def roundness(contour):
        """ Circularity of the contour corrected by the aspect ratio.

        Refs:
            https://progearthplanetsci.springeropen.com/articles/10.1186/s40645-015-0078-x

        Args:
            contour: Contour defined by a list of points

        Returns:
            Circularity of the contour corrected by the aspect ratio
        """
        return round(4 * Contours.area(contour) / (
                math.pi * Contours.major_axis(contour) * Contours.major_axis(contour)), 2)

    @staticmethod
    def circularity(contour):
        """ Circularity of the contour corrected by the aspect ratio.

        Args:
            contour: Contour defined by a list of points

        Returns:
            Circularity of the contour corrected by the aspect ratio
        """
        return round(4 * math.pi * Contours.area(contour) / (Contours.perimeter(contour) *
                                                             Contours.perimeter(contour)), 2)

    @staticmethod
    def solidity(contour):
        """ Calculates the solidity of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            Solidity of the contour
        """
        return round(Contours.area(contour) / Contours.convex_hull_area(contour), 2)

    @staticmethod
    def sphericity(contour):
        """ Calculates the sphericity of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            Sphericity of the contour
        """
        return Contours.min_r(contour) / Contours.max_r(contour)

    @staticmethod
    def aspect_ratio(contour):
        """ Calculates the aspect ratio of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            Aspect ratio of the contour
        """

        return round(Contours.major_axis(contour) / Contours.minor_axis(contour), 2)

    @staticmethod
    def area_equivalent_diameter(contour):
        """ Calculates the area equivalent diameter of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            The diameter of the contour of the real area
        """

        return math.sqrt((4 / math.pi) * Contours.area(contour))

    @staticmethod
    def perimeter_equivalent_diameter(contour):
        """ Calculates the perimeter equivalent diameter of the contour.

        Args:
            contour: Contour defined by a list of points
        Returns:
            The diameter of the contour of the real perimeter
        """

        return Contours.perimeter(contour) / math.pi

    @staticmethod
    def equivalent_ellipse_area(contour):
        """ Equivalent ellipse area of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            The area of the equivalent ellipse of the contour
        """
        return math.pi * Contours.major_axis(contour) * Contours.minor_axis(contour)

    @staticmethod
    def compactness(contour):
        """ Calculates the compactness of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            The compactness of the contour
        """
        return math.sqrt((4 * Contours.area(contour)) / math.pi) / Contours.major_axis(contour)

    @staticmethod
    def concavity(contour):
        """ Calculates the concavity of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            The concavity of the contour
        """
        return Contours.convex_hull_area(contour) - Contours.area(contour)

    @staticmethod
    def convexity(contour):
        """ Calculates the convexity of the contour.

        The convexity is a measure of the curvature of an object. Is calc by the relation between
        the perimeter of the convex hull and the perimeter of the object.

        Args:
            contour: Contour defined by a list of points
        Returns:
            The convexity of the contour
        """
        return Contours.convex_hull_perimeter(contour) / Contours.perimeter(contour)

    @staticmethod
    def shape(contour):
        """ Calculates the shape of the contour.

        Relation between perimeter and area. Calc the elongation of an object

        Args:
            contour: Contour defined by a list of points
        Returns:
            The shape of the contour
        """
        return math.pow(Contours.perimeter(contour), 2) / Contours.area(contour)

    @staticmethod
    def shape_factor_1(contour):
        """ Calculates the shape factor 1 of the contour.

        Args:
            contour: Contour defined by a list of points
        Returns:
            The shape factor 1 of the contour
        """
        _, _, w, h = Contours._bounding_box(contour)

        return min(w, h) / max(w, h)

    @staticmethod
    def r_factor(contour):
        """ Calculates the r factor of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            The r factor of the contour
        """
        return Contours.convex_hull_perimeter(contour) / (Contours.major_axis(contour) * math.pi)

    @staticmethod
    def eccentricity(contour):
        """ Calculates the eccentricity of the contour.

        Calc how much the conic section deviates from being circular. For any point of a conic
        section, the distance between a fixed point F and a fixed straight line l is always equal
        to a positive constant, the eccentricity. Is calculed by the relation between the two
        diagonals of the ellipse.

        Args:
            contour: Contour defined by a list of points

        Returns:
            Ecentricity of the contour
        """
        ellipse = cv2.fitEllipse(contour)
        D = math.fabs((ellipse[0][0] - ellipse[1][0]))
        d = math.fabs(ellipse[0][1] - ellipse[1][1])

        return round((min(d, D) / max(d, D)), 2)

    @staticmethod
    def max_feret(contour):
        """ The maximum Feret diameter of the contour.

        The maximum distance between parallel tangents to the projection area of the contour

        Args:
            contour: Contour defined by a list of points

        Returns:
            The maximum Feret diameter of the contour
        """
        feret, _ = Contours._max_min_feret(contour)
        return feret

    @staticmethod
    def min_feret(contour):
        """ Calculate minimum Feret diameter of the contour.

        The minimum distance between parallel tangents to the projection area of the contour

        Args:
            contour: Contour defined by a list of points

        Returns:

        """
        _, feret = Contours._max_min_feret(contour)
        return feret

    @staticmethod
    def elongation(contour):
        """ Calculate the elongation of the contour.

        Relation between maximum and minimum feret of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            The elongation of the contour
        """
        return Contours.max_feret(contour) / Contours.min_feret(contour)

    @staticmethod
    def hu_moments(contour):
        """ Calculate the Hu moments of the contour.

        Args:
            contour: Contour defined by a list of points

        Returns:
            The Hu moments of the contour
        """
        return cv2.HuMoments(cv2.moments(contour)).flatten()

    @staticmethod
    def center(contour):
        """ Calculate the center of the contour.

        The centroid of a plane figure is the arithmetic mean of all the point in the figure. For
        calculate it we use the moments of the image

        Refs:
            https://en.wikipedia.org/wiki/Image_moment.
        Args:
            contour: Contour defined by a list of points

        Returns:
            The center of the contour
        """
        moments = cv2.moments(contour)
        center_x = int(moments['m10'] / moments['m00'])
        center_y = int(moments['m01'] / moments['m00'])

        return center_x, center_y

    @staticmethod
    def _max_min_feret(contour):
        """ Calculate the maximum and minimum Feret diameter of the contour.

        Helper method for calculation of maximum and minimum ferets based on convex hull of the
        contour. Based on C++ code: https://www.crisluengo.net/archives/408

        Args:
            contour: Contour defined by a list of points
        Returns:
              Maximum and minimum feret of the contour
        """
        convex_hull_contour = Contours.convex_hull(contour)
        min_feret = 999999
        max_feret = 0
        n = len(convex_hull_contour) - 1
        p0 = n
        p = 0
        q = 1

        while Contours._triangle_area(convex_hull_contour[p][0],
                                      convex_hull_contour[Contours._next_point(p, n)][0],
                                      convex_hull_contour[Contours._next_point(q, n)][0]) > \
                Contours._triangle_area(convex_hull_contour[p][0],
                                        convex_hull_contour[Contours._next_point(p, n)][0],
                                        convex_hull_contour[q][0]):
            q = Contours._next_point(q, n)

        while p != p0:
            p = Contours._next_point(p, n)
            listq = [q]
            while Contours._triangle_area(convex_hull_contour[p][0],
                                          convex_hull_contour[Contours._next_point(p, n)][0],
                                          convex_hull_contour[Contours._next_point(q, n)][0]) > \
                    Contours._triangle_area(convex_hull_contour[p][0],
                                            convex_hull_contour[Contours._next_point(p, n)][0],
                                            convex_hull_contour[q][0]):
                q = Contours._next_point(q, n)
                listq.append(q)

            if Contours._triangle_area(convex_hull_contour[p][0],
                                       convex_hull_contour[Contours._next_point(p, n)][0],
                                       convex_hull_contour[Contours._next_point(q, n)][0]) == \
                    Contours._triangle_area(convex_hull_contour[p][0],
                                            convex_hull_contour[Contours._next_point(p, n)][0],
                                            convex_hull_contour[q][0]):
                listq.append(Contours._next_point(q, n))

            for i in range(len(listq)):
                q = ((listq[i] - 1) % n) + 1
                d = math.sqrt((convex_hull_contour[p][0][0] - convex_hull_contour[q][0][0]) ** 2 +
                              (convex_hull_contour[p][0][1] - convex_hull_contour[q][0][1]) ** 2)
                if d > max_feret:
                    max_feret = d

            p3 = convex_hull_contour[p][0]
            for i in range(len(listq) - 2):
                p1 = convex_hull_contour[listq[i]][0]
                p2 = convex_hull_contour[listq[i + 1]][0]
                height = Contours._triangle_height(p1, p2, p3)

                if height < min_feret:
                    min_feret = height

        return max_feret, min_feret

    @staticmethod
    def _triangle_area(point_1, point_2, point_3):
        """ Calculate the area of a triangle given by three points.

        Helper method that calculates triangle area based on triangle vertices

        Args:
            point_1: First point of the triangle
            point_2: Second point of the triangle
            point_3: Third point of the triangle

        Returns:
            The area of the triangle
        """
        return ((point_2[0] - point_1[0]) * (point_3[1] - point_1[1]) -
                (point_2[1] - point_1[1]) * (point_3[0] - point_1[0])) / 2

    @staticmethod
    def _triangle_height(point_1, point_2, point_3):
        """ Calculate the height of a triangle given by three points.

        Args:
            point_1: First vertex of the triangle
            point_2: Second vertex of the triangle
            point_3: Third vertex of the triangle

        Returns:
            The height of the triangle
        """
        return ((point_2[0] - point_1[0]) * (point_3[1] - point_1[1]) -
                (point_2[1] - point_1[1]) * (point_3[0] - point_1[0])) / \
               math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

    @staticmethod
    def _next_point(point, n_points):
        """ Get the next antipodal point in the contour.

        Args:
            point: Previous point in the contour
            n_points: Total number of points in the contour

        Returns:
            The next antipodal point in the contour
        """
        return point % n_points + 1
