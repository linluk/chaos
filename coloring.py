#!/usr/bin/env python
"""
Filename: coloring.py
Author: Lukas Singer <lukas42singer (at) gmail (dot) com>
Created: 2016/06/09
Copyright: 2016, Lukas Singer
License: WTFPL (see COPYING or <http://www.wtfpl.net/>)
Description: This module contains the coloring functions.
"""

import collections
# TODO: implement more coloring algorithms:
#       here are some: http://www.eddaardvark.co.uk/python_patterns/schemes.html

# TODO: refactor so that itermax is not needed as a parameter to the coloring
#       functions. it is constant and can be passed to the factory function
#       instead.

# TODO: consider this link when experimenting with colors:
#       http://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion

colorings = None

def simple_modulo(inside_color, *colors):
    l = len(colors)
    def f(complex_coord, complex_value, iter_max, iter_count):
        if iter_count >= iter_max:
            return inside_color
        else:
            return colors[iter_count % l]
    return f

def simple_shading(inside_color, start_color, stop_color, iter_max):
    delta = ((stop_color[0] - start_color[0]) / iter_max,
             (stop_color[1] - start_color[1]) / iter_max,
             (stop_color[2] - start_color[2]) / iter_max)
    def f(complex_coord, complex_value, iter_max, iter_count):
        if iter_count >= iter_max:
            return inside_color
        else:
            return (int(start_color[0] + iter_count * delta[0]),
                    int(start_color[1] + iter_count * delta[1]),
                    int(start_color[2] + iter_count * delta[2]))
    return f


def initialize():
    global colorings
    colorings = collections.OrderedDict([
        ('Default', lambda *_: None),
        ('Modulo 2', lambda *_: simple_modulo((0, 0, 0),
                                           (255, 0, 0),
                                           (0, 0, 255))),
        ('Modulo 3', lambda *_: simple_modulo((0, 0, 0),
                                           (255, 0, 0),
                                           (0, 255, 0),
                                           (0, 0, 255))),
        ('Simple Shading', lambda max_iter, *_: simple_shading(
            (255, 255, 255),
            (255, 255, 255),
            (0, 0, 0),
            max_iter))])
