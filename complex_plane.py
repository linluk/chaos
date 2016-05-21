#!/usr/bin/env python

from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk

import tkinter as tk

class ComplexPlane:

  class ComplexPlaneIterator:

    def __init__(self, pixel_size, p2c):
      """ creates the iterator for complex planes """
      super().__init__()
      self.p2c = p2c
      self.w, self.h = pixel_size
      self.p = 0, -1 # we inc first

    def __iter__(self):
      """ an iterator has to return itself as an iterator """
      return self

    def __next__(self):
      """ returns the next pair of pixel- and complex coord """
      x, y = self.p
      y += 1
      if y >= self.w:
        y = 0
        x += 1
        if x >= self.h:
          raise StopIteration()
      self.p = (x, y)
      return self.p2c(self.p), self.p

  def __init__(self,
               pixel_size=(320, 240),   # size of the plane on the screen
               complex_size=(3.2, 2.4), # size of the complex plane
               pixel_origin=None):      # pixel position of (0 + 0j)
    """ creates a complex plane """
    super().__init__()
#    self.image = tk.PhotoImage(width=pixel_size[0], height=pixel_size[1])
    self.img = Image.new("RGB", pixel_size)
    self.draw = ImageDraw.Draw(self.img)
    if not pixel_origin:
      pixel_origin = (pixel_size[0] // 2, pixel_size[1] // 2)
    self.pixel_origin = pixel_origin
    self.pixel_delta = (complex_size[0] / pixel_size[0],
                        complex_size[1] / pixel_size[1])

  def __iter__(self):
    return ComplexPlane.ComplexPlaneIterator(
      #(self.image.width(), self.image.height()),
      self.img.size,
      self.p2c)

  def c2p(self, z):
    """ returns the pixel coord for complex z """
    z = complex(z)
    p = (int((z.real / self.pixel_delta[0] + self.pixel_origin[0]) + 0.5),
         int((z.imag / self.pixel_delta[1] + self.pixel_origin[1]) + 0.5))
    return p

  def p2c(self, p):
    """ returns the complex coord for pixel p """
    z = complex((p[0] - self.pixel_origin[0]) * self.pixel_delta[0],
                (p[1] - self.pixel_origin[1]) * self.pixel_delta[1])
    return z

  def set_pixel(self, p, color):
    """ sets the pixel p to color """
#    self.image.put(color, p)
    self.draw.point(p, color)

#  def get_pixel(self, p):
#    """ returns the color of pixel p """
#    return self.image.get(p)

  def set_complex(self, z, color):
    """ sets the corresponding pixel of complex z to color """
    self.set_pixel(self.c2p(z), color)

#  def get_complex(self, z):
#    """ returns the color of the pixel coresponding to complex z """
#    return self.get_pixel(self.c2p(z))

  def pixels_as_complex(self):
    """ iterates over all pixels as complex numbers """
    for x in range(self.image.width()):
      for y in range(self.image.height()):
        yield self.p2c((x, y))

  def get_tk_image(self):
    """ i hate this function, ... """
#    return self.image
    return ImageTk.PhotoImage(self.img)
