#!/usr/bin/env python
"""
Filename: mandelbrot.py
Author: Lukas Singer <lukas42singer (at) gmail (dot) com>
Created: 2016/05/25
Copyright: 2016, Lukas Singer
License: WTFPL (see COPYING or <http://www.wtfpl.net/>)
Description: Mandelbrot set algorithm and coloring.
"""

import time

import complex_plane

def mandelbrot(width, height,
               start, end,
               coloring=None,
               bailout=2.0,
               itermax=256):
    # i found this link. maybe its worth trying it to improve speed.
    #   http://www.tutorialspoint.com/python/python_further_extensions.htm
    # HINT: i would just write the code for a single pixel in c.
    #   the function should/could take the complex number, bailout and iter_max
    #   and return the number of iterations.
    t0 = time.clock()
    cp = complex_plane.ComplexPlane(width, height, start, end)
    if not coloring:
        coloring = DEFAULT_COLORING
    for c, p in cp:
        # we should start with z = 0 and i = 0
        # but after one iteration we always have
        # z = c and i = 1, so we could start with that
        # saving one iteration per pixel.
        z = c
        i = 1
        while abs(z) < bailout and i < itermax:
            z = z * z + c
            i += 1
        cp.set_pixel(p, coloring(c, z, itermax, i))
    t1 = time.clock()
    print('rendered mandelbrot in {:.3g} seconds'.format(t1 - t0))
    return cp

###############################################################################
###   COLORING   ##############################################################
###############################################################################

# TODO: implement more coloring algorithms:
#       here are some: http://www.eddaardvark.co.uk/python_patterns/schemes.html

# TODO: refactor so that itermax is not needed as a parameter to the coloring
#       functions. it is constant and can be passed to the factory function
#       instead.

# TODO: consider this link when experimenting with colors:
#       http://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion

def modulo_coloring(inside_color, *colors):
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

DEFAULT_COLORING =  modulo_coloring(
    (0, 0, 0),
    (255, 255, 255),
    (0, 0, 0))
