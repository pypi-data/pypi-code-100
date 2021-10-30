#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/matplotgraphs.py

    Draw graphs using matplotlib.

    Code largely inspired by
        https://matplotlib.org/stable/gallery/lines_bars_and_markers/gradient_bar.html

    ___________________________________________________________________________

    o  gradient_image(axes, extent, direction=0.5, cmap_range=(0, 1), **kwargs)
    o  gradient_bar(axes, pos_x, pos_y, height=0.4, left=0)
    o  hbar2png(_data, filename, unit, title, fmtstring, value_coeff)
"""
from matplotlib import pyplot
import numpy as np

import wisteria.globs


def gradient_image(axes,
                   extent,
                   direction=0.5,
                   cmap_range=(0, 1),
                   **kwargs):
    """
        gradient_image()

        Draw a gradient image based on a colormap.

            Code largely inspired by
                https://matplotlib.org/stable/gallery/lines_bars_and_markers/gradient_bar.html

        _______________________________________________________________________

        ARGUMENTS:
        o  (matplotlib.axes._subplots.AxesSubplot) axes: axes to draw on
        o  (tuple of 4 floats)                   extent: the extent of the image,
                                                         (xmin, xmax, ymin, ymax),
                                                         expressed in in Axes coordinates
        o  (float)                            direction: direction of the gradient, a
                                                         number in range 0 (=vertical)
                                                         to 1 (=horizontal)
        o  (float, float)                    cmap_range: fraction (cmin, cmax) of the colormap that
                                                         should be used for the gradient, where the
                                                         complete colormap is (0, 1)
        o                                      **kwargs: other parameters are passed on to
                                                         `.Axes.imshow()`, in particular:
                o (str or Colormap)                cmap: Colormap instance or registered colormap
                                                         name used to map scalar data to colors.
    """
    phi = direction * np.pi / 2
    vector = np.array([np.cos(phi), np.sin(phi)])
    image = np.array([[vector @ [1, 0], vector @ [1, 1]],
                      [vector @ [0, 0], vector @ [0, 1]]])
    cmin, cmax = cmap_range
    image = cmin + (cmax - cmin) / image.max() * image
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html
    axes.imshow(image, extent=extent, interpolation='bicubic',
                vmin=0, vmax=1, **kwargs)


def gradient_bar(axes,
                 pos_x,
                 pos_y,
                 height=0.4,
                 left=0):
    """
        Draw a rectangle using gradient_image().

            Code largely inspired by
                https://matplotlib.org/stable/gallery/lines_bars_and_markers/gradient_bar.html

        _______________________________________________________________________

        ARGUMENTS:
        o  (tuple of float-s)pos_x : for each item, rightest x position (=right)
        o  (tuple of float-s)pos_y : for each item, highest y position (=bottom; here top > bottom)
        o  (float)height: height of the bar
        o  (float)left  : leftest x position
    """
    for right, bottom in zip(pos_x, pos_y):
        top = bottom + height

        # Pylint doesn't seem to know pyplot.cm.* members:
        #   pylint: disable=no-member
        gradient_image(axes, extent=(left, right, bottom - 0.4, top),
                       cmap=pyplot.cm.Reds_r, cmap_range=(0, 0.8))


def hbar2png(results_hall_attribute,
             filename,
             unit,
             title,
             fmtstring,
             value_coeff):
    """
            Create a graph with horizontal bars from <results_hall_attribute> and write in
            <filename>.

            Code largely inspired by
                https://matplotlib.org/stable/gallery/lines_bars_and_markers/gradient_bar.html

            ___________________________________________________________________

            ARGUMENTS:
            o  (list of (value, serializer name))results_hall_attribute: content of
                                                                         results.hall[attribute]
            o  (str)                                           filename: path to the file to be
                                                                         written
            o  (str)                                               unit: unit of values to be
                                                                         printed on the graph
            o  (str)                                              title: title of the graph
            o  (str)                                          fmtstring: format string to be applied
                                                                         to each value when printed
                                                                         on the graph; e.g. '{0}' or
                                                                         '{0:.1f}' .
            o  (float)                                      value_coeff: each value will be
                                                                         multiplied by this number.
    """
    pyplot.rcdefaults()
    pyplot.rcParams.update({'axes.labelsize': 'large',
                            'xtick.labelsize': 'x-small',
                            'ytick.labelsize': 'large',
                            })

    length = len(results_hall_attribute)
    values = tuple(item[0] for item in results_hall_attribute)
    serializers_names = tuple(
        wisteria.globs.SERIALIZERS[item[1]].human_name for item in results_hall_attribute)

    xlim = 0, max(values)*1.2  # = xmin, xmax
    ylim = -1, length  # = ymin, ymax

    fig, axes = pyplot.subplots()
    fig.subplots_adjust(left=0.35)
    axes.set(xlim=xlim, ylim=ylim, autoscale_on=False)

    # background image:
    # Pylint doesn't seem to know pyplot.cm.* members:
    #   pylint: disable=no-member
    gradient_image(axes, direction=0.1, extent=(0, 1, 0, 1), transform=axes.transAxes,
                   cmap=pyplot.cm.Blues, cmap_range=(0.1, 0.6))

    # bars:
    gradient_bar(axes, values, range(length))
    axes.set_title(title)
    for value_index, value in enumerate(values):
        axes.text(value,
                  value_index,
                  "  " + fmtstring.format(value*value_coeff),
                  color='red',
                  va='center',
                  fontsize=9, fontweight='normal')

    axes.set_xlabel(unit)
    axes.set_aspect('auto')
    pyplot.yticks(range(length), serializers_names)
    axes.set_yticks(range(length))

    pyplot.savefig(filename)
