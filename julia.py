#!/usr/bin/env python
"""
Filename: julia.py
Author: Lukas Singer <lukas42singer (at) gmail (dot) com>
Created: 2016/05/27
Copyright: 2016, Lukas Singer
License: WTFPL (see COPYING or <http://www.wtfpl.net/>)
Description: Julia set algorithm and coloring.
"""

import complex_plane

def julia(width, height,
          start, end,
          c,
          coloring=None,
          bailout=2.0,
          itermax=256):
    cp = complex_plane.ComplexPlane(width, height, start, end)
    if not coloring:
        def coloring(c, z, m, i):
            if i >= m:
                return (0, 0, 0)
            elif i % 2 == 0:
                return (255, 0, 0)
            else:
                return (0, 0, 255)
    for z0, px in cp:
        zn = z0
        i = 0
        while abs(zn) < bailout and i < itermax:
            zn = zn * zn + c
            i += 1
        cp.set_pixel(px, coloring(c, zn, itermax, i))
    return cp
